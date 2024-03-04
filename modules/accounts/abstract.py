from abc import ABC, abstractmethod

import time
import json
import requests

from modules.databases.manager_main import DatabaseManager


class Account(ABC):
    """
    Classe abstrata que representa uma conta genérica e gerencia a sessão de autenticação.

    Atributos e métodos desta classe devem ser estendidos por classes específicas
    de plataformas de cursos.
    """

    def __init__(self, account_id: int = 0):
        self.account_id = account_id
        self.username = ''
        self.password = ''
        self.is_valid = False
        self.validated_at = 0
        self.has_authenticated = False
        self.authenticated_at = 0
        self.auth_token = ''
        self.auth_token_expires_at = 0
        self.refresh_token = ''
        self.refresh_token_expires_at = 0
        self.other_data = ''
        self._database_manager = DatabaseManager()
        self.session = self._restart_requests_session()
        self.load_account_information()

    def _restart_requests_session(self) -> requests.Session:
        """
        Inicia uma sessão limpa da biblioteca requests.

        :return: Sessão da biblioteca requests com o User-Agent configurado.
        """
        session = requests.Session()
        settings = self._database_manager.get_all_settings()
        session.headers['User-Agent'] = settings.get('default_user_agent',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0')
        return session
    
    def get_current_time(self) -> int:
        """
        Retorna o tempo atual em segundos.
        """
        return int(time.time())

    def dump_json_data(self, data) -> str:
        """
        Serializa dados da conta em formato JSON.
        """
        return json.dumps(data, indent=4, ensure_ascii=False)

    def load_account_information(self) -> None:
        """
        Configura os atributos da conta com informações do banco de dados.
        """
        data = self._database_manager.execute_query("""
            SELECT username, password, added_at, is_valid, last_validated_at WHERE id = ?""",
            (self.account_id,), fetchone=True)
        self.username = data[0]
        self.password = data[1]
        self.is_valid = bool(data[3])
        self.validated_at = data[4]
    
    @abstractmethod
    def get_platform_id(self) -> int:
        """
        Retorna o ID da plataforma de cursos.
        """
    
    @abstractmethod
    def login(self):
        """
        Método abstrato para realizar o login na plataforma.
        """

    @abstractmethod
    def get_account_products(self):
        """
        Método abstrato para obter os produtos associados à conta.
        """

    @abstractmethod
    def get_product_information(self, product_id):
        """
        Método abstrato para obter informações de um produto específico.
        """
