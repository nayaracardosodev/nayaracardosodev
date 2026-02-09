class ContaBancaria:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.saldo = saldo

    def ver_extrato(self):
        print(f"Extrato de {self.titular}: R$ {self.saldo:.2f}")

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            print(f"{self.titular}, o saque de R$ {valor} realizado com sucesso!")
        else:
            print(f"{self.titular}, seu saldo é insuficiente :(")

    def dinheiro_chegando(self, valor):
        self.saldo += valor
        print(f'{self.titular}, você acaba de receber R${valor:.2f} com sucesso!')

    def transferir(self, valor, conta_destino):
        if valor <= self.saldo:
            self.saldo -= valor
            conta_destino.dinheiro_chegando(valor)
            self.saldo += 0.01
            print(f"✅ Transferência feita para {conta_destino.titular}! {self.titular} você ganhou R$ 0.01 de cashback e seu saldo atual é de R${self.saldo:.2f}.")
        else:
            print(f"🚫 {self.titular}, seu saldo é insuficiente para transferir.")


class ContaCorrente(ContaBancaria):
    def __init__(self, titular, saldo, limite):
        super().__init__(titular, saldo)
        self.limite = limite

    def usar_limite(self):
        print(f"{self.titular}, você tem R$ {self.saldo} de saldo e R$ {self.limite} de limite extra.")

    def sacar(self, valor):
        valor_taxa = 2

        if (valor + valor_taxa) <= self.saldo:
            super().sacar(valor)
            self.saldo -= valor_taxa
            print(f"Descontada taxa de serviço: R$ {valor_taxa:.2f}")
        else:
            print(f"{self.titular}, seu saldo para saque de R$ {valor} + taxa de R$ {valor_taxa} é insuficiente. :(")

class ContaPoupanca(ContaBancaria):
    def __init__(self, titular, saldo, taxa_rendimento_porcentagem):
        """
        ATENÇÃO: Coloque a taxa inteira!
        Exemplo: Digite 5 para 5%.
        """
        super().__init__(titular, saldo)
        self.taxa_rendimento = taxa_rendimento_porcentagem / 100

    def render_dinheiro(self):
        rendimento = self.saldo * self.taxa_rendimento
        self.saldo += rendimento
        print(f"Oba! {self.titular}, seu dinheiro rendeu R$ {rendimento:.2f}.")
        print(f"{self.titular}, o novo saldo em sua poupança é: R$ {self.saldo:.2f}")

contac_kevin = ContaCorrente('Kevin', 2000, 1000)
contac_kevin.usar_limite()
contac_kevin.sacar(2000)

print("-" * 50)

minha_contap = ContaPoupanca('Nayara', 2000, 5)
minha_contap.render_dinheiro()
minha_contap.ver_extrato()

print("-" * 50)

contap_kevin = ContaPoupanca('Kevin', 49000, 1.16)
contap_kevin.render_dinheiro()
contap_kevin.ver_extrato()

print("-" * 50)

contap_kevin = ContaPoupanca('Kevin', 49000, 1.16)
contap_kevin.transferir(1000, minha_contap)

print("-" * 50)