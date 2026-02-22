# Open Claw — Architecture iOS hybride pour agents IA open source

## 1) Vision produit

**Open Claw** est une application iOS de gestion de dépôts (documents, artefacts, configurations d'agents) qui permet:

- l'exécution **locale** d'agents IA open source pour confidentialité et autonomie,
- la connexion **optionnelle** à des IA/services publics (API cloud) pour des tâches lourdes,
- une orchestration unifiée des agents via une interface claire et modulaire.

Le principe est **local-first**: l'application fonctionne sans réseau, puis active les intégrations externes uniquement lorsque l'utilisateur le décide.

---

## 2) Exigences couvertes

### A. Architecture modulaire des agents

- Système de plugins d'agents via un protocole `AgentPlugin`.
- Registre dynamique (`AgentRegistry`) pour charger/activer des agents sans modifier le cœur applicatif.
- Contrats communs pour:
  - découverte de capacités,
  - exécution synchrones/asynchrones,
  - gestion des politiques (offline-only, cloud-allowed, etc.).

### B. Paramètres configurables optimisés iOS local

- Profils de performance selon appareil (`Eco`, `Balanced`, `Performance`).
- Paramètres par agent:
  - taille de contexte,
  - batch size,
  - quantization (4-bit/8-bit),
  - seuil mémoire/CPU.
- Auto-tuning selon:
  - modèle de device,
  - batterie,
  - température,
  - état Low Power Mode.

### C. Synchronisation sécurisée avec services publics

- Chiffrement au repos (Keychain + fichiers chiffrés).
- TLS + certificate pinning pour endpoints critiques.
- Jetons API stockés en Secure Enclave/Keychain.
- File d'attente de sync avec reprise sur incident et politique zero-trust.

### D. Interface claire de gestion d'agents

- Catalogue d'agents installés/disponibles.
- État visuel: actif, inactif, local-only, hybride.
- Éditeur de configuration par agent avec presets.
- Traces d'exécution lisibles + mode diagnostic.

### E. Performance adaptée aux mobiles

- Priorisation QoS, exécution incrémentale, cancellation cooperative.
- Cache sémantique local + eviction LRU.
- Compression des artefacts et synchronisation différentielle.
- Budgets CPU/RAM configurables par tâche.

---

## 3) Architecture technique (vue logique)

```text
┌─────────────────────────────────────────────────────────┐
│                    UI Layer (SwiftUI)                  │
│ Dashboard · Agent Manager · Sync Center · Settings     │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                Application Core (Domain)               │
│ UseCases · Policies · Feature Flags · Telemetry        │
└───────┬───────────────────────┬─────────────────────────┘
        │                       │
┌───────▼────────────┐  ┌───────▼────────────────────────┐
│ Agent Runtime      │  │ Sync & Connectivity Layer      │
│ Registry           │  │ Secure API Connectors          │
│ Scheduler          │  │ Queue/Retry/Conflict Resolver  │
│ Resource Governor  │  │ Trust & Consent Policies       │
└───────┬────────────┘  └──────────────┬──────────────────┘
        │                              │
┌───────▼──────────────────────────────────────────────┐
│              Data Layer & Security                   │
│ Core Data/SQLite · FileStore · Keychain · CryptoKit │
└──────────────────────────────────────────────────────┘
```

---

## 4) Modules principaux

## 4.1 `AgentKit` (modulaire)

### Protocole d'agent

```swift
public protocol AgentPlugin {
    var id: String { get }
    var displayName: String { get }
    var capabilities: [AgentCapability] { get }

    func configure(_ config: AgentConfig) throws
    func validateResources() -> AgentHealth
    func run(task: AgentTask, context: AgentContext) async throws -> AgentResult
}
```

### Responsabilités
- Uniformiser l'intégration de modèles OSS (LLM, classifieurs, extracteurs).
- Isoler les dépendances natives (Core ML, llama.cpp bindings, ONNX Runtime Mobile).
- Permettre des mises à jour d'agents sans casser le noyau.

## 4.2 `RuntimeOrchestrator`

- Planifie les exécutions (`TaskPriority`, deadlines, quotas).
- Dirige vers local ou cloud selon:
  - politique utilisateur,
  - niveau de sensibilité des données,
  - disponibilité réseau,
  - coût latence/énergie.
- Applique un **Policy Engine**:
  - `StrictLocal`: jamais de cloud,
  - `HybridGuarded`: cloud possible si consentement explicite,
  - `CloudAssist`: fallback cloud automatique sur timeout local.

## 4.3 `SyncGuard`

- Synchronisation bidirectionnelle des dépôts/configs.
- Journal d'opérations signé (integrity log).
- Résolution de conflits (Last Writer Wins configurable ou merge métier).
- Support mode hors-ligne prolongé avec replay différé.

## 4.4 `ResourceGovernor`

- Surveille RAM/CPU/thermals/batterie.
- Adapte dynamiquement:
  - tokens max,
  - threads,
  - fréquence de sync,
  - taille de modèles chargés.
- Déclenche **graceful degradation** si surcharge.

---

## 5) Flux d'exécution hybride

1. L'utilisateur lance une tâche sur un agent.
2. `RuntimeOrchestrator` évalue la politique de confidentialité.
3. Si local autorisé et ressources suffisantes -> exécution locale.
4. Si local insuffisant et cloud autorisé -> anonymisation + appel connecteur public.
5. Résultat consolidé, journalisé, puis stocké localement.
6. Sync éventuelle selon stratégie (immédiate, différée, manuelle).

---

## 6) Modèle de sécurité

- **Privacy tiers** pour les données:
  - Tier 1: strictement local,
  - Tier 2: local + métadonnées synchronisables,
  - Tier 3: cloud autorisé.
- Consentement granulaire par agent et par type d'opération.
- Rotation de clés et expiration des sessions.
- Audit local exportable (conformité, forensic).

---

## 7) UX recommandée

- **Écran “Agents”**:
  - liste, recherche, tags de capacités,
  - bouton activer/désactiver,
  - badge “Local”, “Hybride”, “Cloud”.
- **Écran “Performance”**:
  - profil global,
  - usage ressources en temps réel,
  - suggestions automatiques d'optimisation.
- **Écran “Connectivité”**:
  - endpoints configurés,
  - santé des services,
  - dernière sync + erreurs actionnables.
- **Écran “Confidentialité”**:
  - politique active,
  - permissions accordées,
  - journal des transferts externes.

---

## 8) Optimisations iOS concrètes

- Utiliser `BGTaskScheduler` pour sync différée non bloquante.
- Préférer `URLSession` background pour uploads/downloads robustes.
- Exploiter `os_signpost` + Instruments pour profiler latence/énergie.
- Charger les modèles à la demande (lazy load) + unloading agressif.
- Gérer les pics mémoire avec batching et streaming token par token.

---

## 9) Stack technique suggérée

- **UI**: SwiftUI + Combine/Observation.
- **Concurrence**: Swift Concurrency (`async/await`, actors).
- **Données**: Core Data ou SQLite (GRDB) + FileManager chiffré.
- **Sécurité**: CryptoKit, Keychain, Secure Enclave.
- **IA locale**:
  - Core ML pour modèles convertis,
  - ONNX Runtime Mobile,
  - bindings llama.cpp (si besoin LLM quantifié).
- **Connecteurs cloud**: couche abstraite compatible OpenAI-compatible APIs, Hugging Face Inference, endpoints privés.

---

## 10) Roadmap de mise en œuvre

### Phase 1 — MVP local
- AgentRegistry + 2 agents locaux (résumé, classification).
- UI de gestion agents.
- Stockage local chiffré.

### Phase 2 — Hybride sécurisé
- SyncGuard + connecteurs publics optionnels.
- Consentements granulaires + journal d'audit.
- Mode fallback cloud contrôlé.

### Phase 3 — Optimisation avancée
- Auto-tuning par appareil.
- Cache sémantique intelligent.
- Diagnostics performances en temps réel.

---

## 11) Critères de succès

- Temps moyen de réponse locale acceptable sur iPhone milieu de gamme.
- Taux d'échec sync < seuil cible avec reprise automatique.
- 100% des transferts externes traçables et explicitement autorisés.
- Satisfaction utilisateur sur lisibilité et contrôle des agents.

---

## 12) Résultat attendu

Cette architecture fournit une solution **hybride, modulaire et privacy-first** pour Open Claw: elle maximise l'autonomie locale sur iOS tout en conservant la flexibilité d'intégrations IA publiques lorsque l'utilisateur y consent.
