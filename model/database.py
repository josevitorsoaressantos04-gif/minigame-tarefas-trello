from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
from datetime import datetime

# =====================================================================
# 1. CONFIGURAÇÕES DO HIBERNATE (SQLAlchemy)
# =====================================================================

# ENGINE: É o motor do banco. É ele quem "fala" fisicamente com o arquivo sqlite.
engine = create_engine('sqlite:///tdah_quest.db', echo=False)

# BASE: É a classe mãe. Toda classe que herdar dela vai ser transformada numa Tabela no banco.
Base = declarative_base()

# SESSION: É a sua "conversa" com o banco. Tudo o que você faz (salvar, apagar) 
# acontece dentro de uma sessão, que só é confirmada quando você dá um "commit".
Session = sessionmaker(bind=engine)


# =====================================================================
# 2. OS NOSSOS MOLDES (Classes = Tabelas)
# =====================================================================

class GameState(Base):
    __tablename__ = 'game_state'  # Nome da tabela no banco
    
    # Cada "Column" é uma coluna na tabela
    id = Column(Integer, primary_key=True)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)

class Log(Base):
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String)
    missao = Column(String)
    dificuldade = Column(String)
    xp_ganho = Column(Integer)
    destino = Column(String)


# =====================================================================
# 3. FUNÇÕES DE ACESSO AOS DADOS (Data Access Object - DAO)
# =====================================================================

def init_db():
    """Cria as tabelas no arquivo se elas não existirem"""
    # Lê todas as classes que herdam de 'Base' e cria as tabelas automaticamente
    Base.metadata.create_all(engine)
    
    # Abre uma conversa com o banco
    session = Session()
    
    # Verifica se já existe um Herói salvo. Se não existir, cria o Herói número 1.
    if not session.query(GameState).first():
        novo_estado = GameState(id=1, xp=0, level=1)
        session.add(novo_estado) # "Prepara" o dado
        session.commit()         # "Salva" de verdade no banco
        
    session.close() # Sempre fechamos a conversa por educação e memória

def load_state():
    """Puxa o XP e Level do Herói com proteção anti-falhas"""
    session = Session()
    estado = session.query(GameState).filter_by(id=1).first()
    
    # Camada de segurança que o Pylance estava a pedir:
    if estado is not None:
        xp_atual = estado.xp
        level_atual = estado.level
    else:
        # Se por acaso o banco estiver vazio, retorna os valores padrão
        xp_atual = 0
        level_atual = 1
        
    session.close()
    return xp_atual, level_atual

def save_state(xp, level):
    """Atualiza o XP e o Nível quando ganhamos pontos"""
    session = Session()
    estado = session.query(GameState).filter_by(id=1).first()
    
    if estado is not None:
        estado.xp = xp
        estado.level = level
        session.commit()
    else:
        # Se o estado não existir, cria um novo no momento de salvar
        novo_estado = GameState(id=1, xp=xp, level=level)
        session.add(novo_estado)
        session.commit()
        
    session.close()

def save_log(missao, dificuldade, xp_ganho, destino):
    """Salva a missão na nossa aba de registros"""
    session = Session()
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Criamos um Objeto "Log" igual criamos um objeto normal em Python
    novo_log = Log(
        data=data_atual,
        missao=missao,
        dificuldade=dificuldade,
        xp_ganho=xp_ganho,
        destino=destino
    )
    
    session.add(novo_log) # Prepara
    session.commit()      # Salva
    session.close()

def load_logs_df():
    """O Pandas é muito amigo do SQLAlchemy. Ele lê a tabela inteira direto do Motor!"""
    # Usamos a conexão do 'engine' para transformar a tabela 'logs' num DataFrame para o Streamlit
    return pd.read_sql_table('logs', con=engine)