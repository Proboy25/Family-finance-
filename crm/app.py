from . import app
import crm.routes  # noqa: F401

if __name__ == '__main__':
    app.run(debug=True)
