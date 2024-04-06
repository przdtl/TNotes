from enum import Enum


class VaultsHandlers(str, Enum):
    REMOVE_BASE_KEYBOARD = '1'


class VaultsCallbackHandlers(str, Enum):
    VAULTS_LIST = 'VAULTS_LIST'
    CREATE_NEW_VAULT = 'CREATE_NEW_VAULT'
    GO_BACK_FROM_CREATE_VAULT = 'GO_BACK_FROM_CREATE_VAULT'
    VAULTS_LIST_PREV_PAGE = 'VAULTS_LIST_PREV_PAGE'
    VAULTS_LIST_NEXT_PAGE = 'VAULTS_LIST_NEXT_PAGE'
    GO_HOME_FROM_VAULTS_LIST = 'GO_HOME_FROM_VAULTS_LIST'
    DELETE_VAULT = 'DELETE_VAULT'
    GO_BACK_FROM_DELETE_VAULT = 'GO_BACK_FROM_DELETE_VAULT'
