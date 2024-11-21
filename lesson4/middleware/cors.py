from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # allow all domain can request your api ( not recommend)
        allow_credentials=True, # allow send cookie or token in request of CORS  (not recommend)
        allow_methods=["*"], # allow all methods: GET , POST, DELETE, PUT, etc..
        allow_headers=["*"], #allow all headers from client
    )