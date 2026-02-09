class Bolo:
    def __init__(self, sabor, fatias):
        self.sabor = sabor
        self.fatias = fatias
        self.cobertura = "Sem cobertura"

    def comer_fatias(self):
        if self.fatias > 0:
            self.fatias -= 1
            print(f"Fatia do bolo de {self.sabor} servida! Restam {self.fatias}.")
        else:
            print("Não tem mais bolo! 😭")

    def colocar_cobertura(self, nova_cobertura):
        self.cobertura = nova_cobertura
        print(f"Oba! Agora o bolo de {self.sabor} tem cobertura de {self.cobertura}!")

bolo1 = Bolo("Chocolate", 20)
bolo2 = Bolo("Laranja", 14)
bolo3 = Bolo("Formigueiro", 16)
bolo4 = Bolo("Cenoura", 18)

bolo1.comer_fatias()
bolo3.colocar_cobertura("Brigadeiro")
bolo1.comer_fatias()
print("\n--- ATENÇÃO: ATAQUE AO BOLO DE LARANJA ---")
for i in range(15):
    bolo2.comer_fatias()