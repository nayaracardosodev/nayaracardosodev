receita_secreta = {
    'nome': 'Bolo de cenoura',
    'preço_venda': 19.00,
    'dimensoes_caixa': ('18', '15', '15'),
    'ingredientes': ['Ovos', 'Óleo', 'Cenoura', 'Açúcar', 'Farinha de trigo', 'Chocolate meio amargo', 'Leite condensado', 'Creme de leite']
}

#receita_secreta['ingredientes'].append('Manteiga sem sal')
#print(f'O doce {receita_secreta['nome']} custa R$ {receita_secreta['preço_venda']} e leva {len(receita_secreta['ingredientes'])} ingredientes.')
#print()
#print(receita_secreta['ingredientes'])
#print()

#for ingrediente in receita_secreta['ingredientes']:
#    print(ingrediente)

#for ingrediente in receita_secreta['ingredientes']:
#    nome_min = ingrediente.lower()

#    if 'leite' in nome_min or 'manteiga' in nome_min or 'chocolate meio amargo' in nome_min:
#        print(f"🚫 CUIDADO: {ingrediente} tem lactose!")
#    else:
#        print(f"✅ {ingrediente} está liberado.")

#for ingrediente in receita_secreta['ingredientes']:
#    if 'leite' in ingrediente.lower() or 'manteiga' in ingrediente.lower() or 'chocolate meio amargo' in ingrediente.lower():
#        print(f"🚫 CUIDADO: {ingrediente} tem lactose!")
#    else:
#        print(f"✅ {ingrediente} está liberado.")

from DetectorLactose import tem_lactose

for item in receita_secreta['ingredientes']:
    if tem_lactose(item):
        print(f"🚫 CUIDADO: {item} tem lactose!")
    else:
        print(f"✅ {item} liberado.")