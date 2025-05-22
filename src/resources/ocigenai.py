import os
import oci
from typing import Dict

class OciGenai:
    def __init__(self):
        self.region = os.getenv('OCI_REGION',default="us-chicago-1")
        self.auth_profile = os.getenv('OCI_AUTH_PROFILE',default='DEFAULT')
        self.auth_type = os.getenv('OCI_AUTH_TYPE',default='API_KEY')
        self.CLIENT_KWARGS = {
            "retry_strategy": oci.retry.DEFAULT_RETRY_STRATEGY,
            "timeout": (10, 240),  # default timeout config for OCI Gen AI service
            }
        if self.auth_type == "API_KEY":
            OCI_CONFIG = oci.config.from_file(profile_name=self.auth_profile)
            signer = oci.signer.Signer(
                tenancy=OCI_CONFIG['tenancy'],
                user=OCI_CONFIG['user'],
                fingerprint=OCI_CONFIG['fingerprint'],
                private_key_file_location=OCI_CONFIG['key_file'],
                pass_phrase=OCI_CONFIG['pass_phrase']
            )
            self.CLIENT_KWARGS.update({'config': OCI_CONFIG})
            self.CLIENT_KWARGS.update({'signer': signer})
        elif self.auth_type == 'INSTANCE_PRINCIPAL':
            OCI_CONFIG = {}
            signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
            self.CLIENT_KWARGS.update({'config': OCI_CONFIG})
            self.CLIENT_KWARGS.update({'signer': signer})

        try:
            self.generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(**self.CLIENT_KWARGS)
        except Exception as error:
            print(f"Controller init failed - {error}")
    
    def split_routes(self,data: Dict = None, endpoint: str = None):
        if endpoint == "chat":
            chat_data = self._invoke_chat(data)
            return chat_data
        elif endpoint == "embedText":
            embed_text_response = self.__embedtext(data)
            return embed_text_response
        
        
        else:
            raise("Not implemented")
    
    def __embedtext(self,data):
        try:
            embed_text_response = self.generative_ai_inference_client.embed_text(data)
            return embed_text_response
        except Exception as error:
            print(f"Error >>> {error}")
        

    def _invoke_chat(self,data): 
        try:
            chat_response = self.generative_ai_inference_client.chat(data)
            return chat_response
        except Exception as error:
            print(f"Error >>> {error}")
        
