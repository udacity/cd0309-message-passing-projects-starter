def register_routes(api, app, root="api"):
    from app.udaconnect import register_routes as attach_person_api

    # Add routes
    attach_person_api(api=api, app=app)
