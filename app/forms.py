from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, DecimalField, BooleanField, IntegerField, TextAreaField    
from wtforms.validators import DataRequired

class RespForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired()])
    cpf = StringField("CPF", validators=[DataRequired()])
    rg = StringField("RG", validators=[DataRequired()])
    telefone = StringField("Telefone")
    email = StringField("e-mail")
    endereco = StringField("Endereço")
    bairro = StringField("Bairro")
    cidade = StringField("Cidade")
    uf = StringField("UF")
    cep = StringField("CEP")
    
    
class ContratoForm(FlaskForm):
    aluno = StringField("Nome", validators=[DataRequired()])
    responsavel = SelectField("Responsável", coerce=int)
    parentesco = StringField("Parentesco", validators=[DataRequired()])
    serie = StringField("Série")
    ano = StringField("Ano")
    data = DateField("Data")
    vencimento = IntegerField("Vencimento", default=5)
    carnet_entregue = BooleanField("Entregou carnê?", default=False)

    mensalidade = DecimalField("Mensalidade", places=2, default=0.0)

    anotacoes = TextAreaField("Anotações")
    
class PrestacaoForm(FlaskForm):
    mes = IntegerField("Mês")
    vencimento = DateField("Vencimento")
    valor = DecimalField("Valor", places=2, default=0.0)

    status = StringField("Situacao")
    data_pgto = DateField("Data de pgto")
    valor_pago = DecimalField("Valor pago", places=2, default=0.0)
    
    forma_de_pgto = StringField("Forma de pgto")
    cheque_numero = StringField("Número do cheque")
    cheque_data = DateField("Data de cheque")


class PagamentoForm(FlaskForm):
    mes = IntegerField("Mês")
    vencimento = DateField("Vencimento")
    valor = DecimalField("Valor", places=2, default=0.0)

    status = StringField("Situacao")
    data_pgto = DateField("Data de pgto")
    valor_pago = DecimalField("Valor pago", places=2, default=0.0)
    
    forma_de_pgto = StringField("Forma de pgto")
    cheque_numero = StringField("Número do cheque")
    cheque_data = DateField("Data de cheque")

