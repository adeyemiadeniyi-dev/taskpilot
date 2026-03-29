from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = ""
    kestra_base_url: str = ""  
    kestra_ui_url: str = ""
    kestra_username: str = ""
    kestra_password: str = ""
    kestra_namespace: str = "main"
    kestra_flow_id: str = "taskpilot_ai_agent"
    kestra_tenant: str = "main"
     
    
    model_config = {
        "env_file": ".env"
    }
        
settings = Settings()