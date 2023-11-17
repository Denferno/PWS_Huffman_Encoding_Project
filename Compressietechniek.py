import heapq
import os
import ast
# In de comments hebben we ook uitleg gedaan als we van dit voorbeeld uitgaan:
def bouw_huffman_boom(tekst):
    # Bereken de frequentie van elk karakter in de tekst
    # Een lege dictionary maken om de frequentie van elk karakter op te slaan
    frequentie = {}
    for letter in tekst:
    # Als het karakter nog niet in de dictionary zit, voeg het toe met een frequentie van 0
        frequentie.setdefault(letter, 0) # https://www.w3schools.com/python/ref_dictionary_setdefault.asp
        frequentie[letter] += 1 
    # De frequentie verhogen met 1 van de huidige letter 
    # We kregen dan zo'n resultaat van de bovenstaande voorbeeld = {'T': 1, 'o': 2, 'b': 1, ' ': 2, e:'3', 'n': 2, 'D': 1}
    # Maak een prioriteitswachtrij (min-heap) op basis van de frequenties. Dit is belangrijk, want het combineert en identificeert de laagste symbolen met elkaar 
    heap = []
    for waarde in frequentie:
        heap.append([frequentie[waarde], [waarde, ""]]) # We willen de letters een tuple vorm hebben, want heapq.heapify accepteert geen dictionaries, alleen tuples.
    # We maken min-heap van de lijst (om ervoor te zorgen dat de laagste frequentie bovenaan staat). Dit doen we met heapify. We hadden geprobeerd dit te doen zonder heapify, maar
    # uiteindelijk kwamen op iets totaal anders uit. Later kwamen we erachter dat we ook simpel heapq.heapify konden gebruiken. Meer info over onze 
    # geschrapte codes staat in onze PO map genaamd 'geschrapte codes' 
    heapq.heapify(heap) 
    # Herhaal totdat je één element over hebt in de heap, want dan is de huffman boom klaar    
    while len(heap) > 1:
        laagste = heapq.heappop(heap) # Haalt steeds de laagste frequentie uit de lijst en verwijderd hem ook uit de lijst
        een_na_laagste = heapq.heappop(heap) # Haalt vervolgens nog een keer de laagste uit de lijst (een na laatste) en verwijderd deze ook uit de lijst
        # De eerste loop wordt laagste = [1, ['D', '']] en een_na_laagste = [1, ['T', '']]
        for paar in laagste[1:]: # laagste[1:] is hier in de eerste iteratie ['D', ''], want '1:' betekent de tweede positie tot het einde van de lijst
            paar[1] = '0' + paar[1] # In de eerste iteratie wordt de paar bijgewerkt door een '0' toe te voegen aan de bestaande code. 
            # Bijvoorbeeld, als de huidige code '1' is, wordt deze gewijzigd in '01'. Het resultaat wordt opgeslagen in de originele lijst: paar[1] = '0' + paar[1].
            # Bij de eerste iteratie wordt paar[1] = ['D','0']
        for paar in een_na_laagste[1:]: # een_na_laagste[1:] is hier in de eerste iteratie[] 
            # Op dezelfde manier wordt de een-na-laagste knoop bijgewerkt door '1' toe te voegen aan de bestaande codes.
            paar[1] = '1' + paar[1]
        # Dit hele proces is vergelijkbaar met aan een rechter tak van een huffman boom een één geven en de linkertak van een huffman boom een 0 geven.
        heapq.heappush(heap, [laagste[0] + een_na_laagste[0]] + laagste[1:] + een_na_laagste[1:]) # Vervolgens combineer je de twee symbolen met elkaar tot één nieuwe symbool.\
    return heap[0][1:] # Uiteindelijk zal dit het resultaat zijn [['T', '00'], ['D', '01'], ['n', '1'], ['o', '10'], ['b', '11'], [' ', '001'], ['e', '000']]

def genereer_huffman_code(boom):
    huffman_code = {}
    for letter, code in boom: # Nu neemt het een letter en een code, dus bij ['T', '00'] wordt letter = 'T' en code = '00'
        huffman_code.setdefault(letter, code) # Vervolgens maken we de lijst naar een dictionary
    return huffman_code 


def tekst_naar_binair(tekst, huffman_code): 
    lst_getallen = [] 
    for letter in tekst: #elk symbool in de tekst wordt een voor een naar een binair getal omgezet, zodat er één zin komt met binaire getallen in plaats van symoblen/letters
        lst_getallen.append(huffman_code[letter])     
    return "".join(lst_getallen)
    


def toegevoegde_waarde_berekenen(binaire_getallen): #als de tekst in binaire code niet deelbaar is door 8 zal de code niet werken, aangezien de symbolen 8 bits nodig hebben om aan de ASCII/UTF-8 eisen te voldoen
    toegevoegde_waarde = 8 - len(binaire_getallen) % 8 #de lengte van de binaire code wordt hier gedeeld door 8. Als deze lengte niet mooi uitkomt, zal de rest waarde worden afgetrokken van het getal 8
    for i in range(toegevoegde_waarde): 
        binaire_getallen += '0' #de restwaarde is dan gelijk aan het aantal toegevoegde nullen, zodat de binaire_getallen deelbaar zijn door 8 en dus een ASCII/UTF-8-symbool kan krijgena
        toegevoegde_info = "{0:08b}".format(toegevoegde_waarde) # Dit zorgt ervoor dat het de 'toegevoegde_waarde' zijn binaire getal krijgt, bijv het getal 2, die krijgt 00000010
        # format zorgt er dus voor dat de 'toegevoegde waarde' zijn binaire getal krijgt
        toegevoegde_tekst = toegevoegde_info + binaire_getallen
    return toegevoegde_tekst

def bouw_byte_lijst(toegevoegde_waarde):
    byte_lijst = []
    for nummer in range(0, len(toegevoegde_waarde), 8): # De loop start van 0 tot en met de lengte van de toegevoegde waarde, (bijv 8), en neemt stappen van 8
    # Stel toegevoegde waarde is hier '0000001000110100', de lengte is dan 16. Er wordt dan 2x gelooped, 1x met nummer = 0, 1x met nummer = 8
        byte = toegevoegde_waarde[nummer:nummer+8]  # De toegevoegde is hier alleen de eerste 8 getallen: '00000010', door nummer+8.  
        byte_lijst.append(int(byte, 2)) # De '2' aan het einde, geeft aan dat de binaire representatie naar een decimale representatie moet worden weergegeven,   
         # dus '00000010', moet een 3 worden. Dit wordt gedaan met de 2 aan het einde bij int(byte, 2). 
    return byte_lijst

    
def compressie(laatste_bytes, huffman_code):
    bestandsnaam_compressie, bestandstype = os.path.splitext(pad) 
    uitvoer_naam_bin = bestandsnaam_compressie +'_compressed' + '.tode'
    uitvoer_naam_dictionary = bestandsnaam_compressie + '_huff_dict' + '.txt'
    with open (uitvoer_naam_dictionary, 'w') as huffman_bestand , open(uitvoer_naam_bin, 'wb') as uitvoer:
        uitvoer.write(laatste_bytes)
        huffman_bestand.write(str(huffman_code))
    print('\nCompressie succesvol')
    print('De bestanden' + bestandsnaam_compressie + 'en'  + uitvoer_naam_dictionary +'zijn aangemaakt')
    return uitvoer_naam_bin
    
def decompressie(invoer_pad, huffman_code):
    bestandsnaam, bestandstype = os.path.splitext(invoer_pad) # Dit is handig, want dan kan ik de bestandsnaam en de bestands extensie van elkaar halen en gebruiken als variabeles
    output_path = bestandsnaam + '_decompressed' + '.txt'
    with open(invoer_pad, 'rb') as file, open(output_path, 'w') as output: 
    # Deze regel opent het invoerbestand (invoer_pad) in binaire modus de ('rb'). Dit staat voor read binary. Op het einde en het uitvoerbestand (output_path) in tekstmodus ('w'). 
    # De with wordt gebruikt om ervoor te zorgen dat beide bestanden correct worden gesloten nadat het codeblok is uitgevoerd.
        bit_string = '' # 
        byte = file.read(1) # leest één byte uit het bestand dat geopend is ('rb'), daarvoor staat die één.
        while byte: 
        # We willen dat zo lang er bytes beschikbaar zijn het blijft lopen, 
        # want dit zorgt ervoor dat de inhoud van het bestand byte voor byte te verwerken is.
        # Dit wordt dan in bit string omgezet naar een binaire representatie met getallen
            byte = ord(byte) # Dit is zodat we de ASCII waarde van een karakter krijgen
            bits = bin(byte)[2:].rjust(8, '0') # Dit zet de ascii waarde om naar binair, dus bijv '1' wordt hier 00000001.
            # De rjust staat voor right justify, het geeft aan dat er nullen worden toegevoegd aan de linker kant totdat er een lengte van 8 heeft.
            bit_string += bits # Deze getallen worden dan toegevoegd aan de bit_string, dus '00000001' wordt toegevoegd aan de lijst bit_string 
            byte = file.read(1) # Hier leest het weer de volgende byte uit het bestand 
        text_after_removing_padding = verwijder_bytes(bit_string)  
        # We hadden bytes toegevoegd bij het comprimeren, dat betekent natuurlijk dat we deze bytes ook van af moeten halen. 
        actual_text = build_ontcijferde_tekst(text_after_removing_padding, huffman_code)
        output.write(actual_text)
    return actual_text 

def verwijder_bytes(tekst):
        bytes_info = tekst[:8] # tekst bijvoorbeeld:  '00000001000101111111111111111110'
        # Alleen de eerste 8 binaire getallen worden toegevoegd aan de bytes_info, want deze eerste 8 waren de toegevoegde waarde 
        #  bij het opbouwen van de bytes hadden we de extra bytes juist aan het begin toegevoegd, dus resultaat is bij het vb hier: bytes_info = '00000001'
        bytes_waarde = int(bytes_info, 2) # Dit hebben we eerder uitgelegd, komt er op neer dat het de '2' ervoor zorgt dat het de bytes info een ascii getal wordt
        # '00000001' wordt 1, want dat is de waarde als je kijkt naar de ASCII tabel
        tekst = tekst[8:-bytes_waarde]  # 
        # Hier wordt de oorspronkelijke binaire tekst aangepast door de eerste 8 bits (byte) te verwdijeren. 
        # Hier is wat er gebeurt:
        # Oorspronkelijke tekst: "000000010001011111111111111111111110"
        # Afsnijden van de eerste 8 bits (bytes_info): "0001011111111111111111111110" 
        # Afsnijden van de laatste 1 bit (bytes_waarde): "000101111111111111111111111"
        return tekst
def build_ontcijferde_tekst(binaire_getallen, huffman_code):
    bits = ''
    ontcijferde_tekst = ''
    
    for bit in binaire_getallen: # binaire getallen zijn bijvoorbeeld: '00010111111111111111111'
        # Dan begint het met een bit waarde van 0
        bits += bit # Deze bit waarde wordt hier toegevoegd aan bits, waardoor bits = '0' wordt
        if bits in huffman_code.values(): # Als de bits in huffman_code overeenkomen met één van de waardes van de dictionary dan pas wordt de volgende stap uitgevoerd
            # ter verduideling hier is een voorbeeld van een dictionary van huffman_code = {'B': '00', 'a': '01', 's': '1'}
            # Bij de eerste iteratie heeft de bit waarde 0 nog geen overeenkomst, dus dan wordt de volgende bit toegevoegd. Dat is in dit voorbeeld een 0.
            # Nu hebben we bits = 00
            # bits == 00 is gelijk aan de waarde '00'
            for k, v in huffman_code.items(): # Dan voert het deze stap uit.
                # De k staat hier voor de 'keys' en de 'v' staat hier voor de 'values'. Een key is bijvoorbeeld een B en de waarde van B is dan 00
                if v == bits: # Met de v wordt gecontroleerd of de v gelijk is aan de bits, en zo ja 
                    ontcijferde_tekst += k # wordt de k toegevoegd aan ontcijferde_tekst, oftewel de sleutel wordt toegevoegd. Dan is in dit geval de B, de sleutel van 00 
                    bits = '' # Hier wordt dan de bits leeggehaald, want we hebben net al de letter B toegevoegd
                    break # Break wordt gedaan zodat het niet verder blijft loopen, want we hebben al de oplossing gevonden. Het heeft geen nut om hem nog harder te laten werken
                # want er is maar één ontcijferde letter mogelijk, dus in dit geval de B.
    return ontcijferde_tekst

def test_input():
    print("Het comprimeren vereist een '.txt' bestand")
    print("Het decomprimeren vereist een de bestandsnaam_huffman_dictionary en een .tode bestand")
    print('Wil je iets comprimeren of handmatig decomprimeren')
    print('Tik C in voor comprimeren en D voor decomprimeren')
    bestandsnaam = input('Tik C in voor comprimeren en D voor decomprimeren: ').lower()
    while True:
            if bestandsnaam == 'c' or bestandsnaam == 'comprimeren':
                print('\nJe hebt gekozen voor comprimeren\n')
                print('Let op:')
                print('Als het bestand in dezelfde folder zit is het pad niet nodig!')
                print('\nVoorbeeld invoer: test.txt')
                while True:
                    pad = input('vul hier de bestandsnaam met het bestandstype in: ')
                    if pad[-4:] == '.txt':
                        return pad
                    else:
                        print("Bestandsnaam moet eindigen op '.txt'. Probeer opnieuw.")
            elif bestandsnaam == 'd' or bestandsnaam =='decomprimeren':
                print('\nJe hebt gekozen voor decomprimeren\n')
                print('Let op dit is alleen mogelijk als je deze twee bestanden heb:')
                print("een '.tode' bestand ")
                print("en de 'huff_dict.txt' bestand")
                handmatig_decomprimeren()
                break
                

def auto_of_hand():
    print('Wil je het automatisch decomprimeren (a) of handmatig decomprimeren (h)?')
    print('Tik a voor automatisch decomprimeren')
    print('Tik h voor handmatig decomprimeren (hier moet je zelf de .tode en dictionary bestand geven)')
    
    while True:
        a_of_h = input("Vul hier de  a  of  h  in: ")
        if a_of_h.lower() == 'a':
            return 'automatisch'
        elif a_of_h.lower() == 'h':
            return 'handmatig'
        else:
            print('Alleen a of h is toegestaan')
            continue
def check_juiste_compressed_file():
    while True: # Deze loop eindigt nooit, totdat er of break wordt uitgevoerd of return 
        compressed_file_pad = input("Vul hier als eerst de '_compressed.tode' bestand in: ")
        if compressed_file_pad[-5:] == '.tode': #[-5], betekent de laatste 5 letters. Als de laatste 5 letters gelijk zijn aan .tode gaat het pas verder
            return compressed_file_pad  
        else:
            print('Incorrect, het moet eindigen op .tode')
            continue # zorgt ervoor dat het verder gaat met de loop
def check_juiste_dictionary():
    while True:
        huffman_code_pad = input("Vul hier het tekstbestand in met de 'huff_dict.txt': ")
        if huffman_code_pad[-13:] == 'huff_dict.txt':
                    return huffman_code_pad
        else:
            print('Incorrect, het moet eindigen op huff_dict.txt')
            continue
        
def handmatig_decomprimeren():
    compressed_file_pad = check_juiste_compressed_file() # Hier wordt gechecked of er wel de juiste bestand wordt ingevoerd
    huffman_dict_pad = check_juiste_dictionary() # Hier wordt gechecked of er wel de huffman bestand wordt ingevoerd
    huffman_bestand = open(huffman_dict_pad) # Hier wordt het huffman bestand geopent
    huffman_dict_string = huffman_bestand.read() # En hier wordt het huffman bestand gelezen, maar het probleem is dat het nu nog in string is.
    huffman_dict = ast.literal_eval(huffman_dict_string) # Zorgt ervoor dat de string naar een normale python dictionary wordt omgezet, dus van '{a:0, b:1}' naar {a:0, b:1} zonder de string
    decompressie(compressed_file_pad, huffman_dict) # De decompressie heeft alleen de binaire waardes nodig en de dictionary voor het decomprimeren

def main():
    tekst_bestand = open(pad)
    tekst = tekst_bestand.read()
    huffman_boom = bouw_huffman_boom(tekst) 
    huffman_code = genereer_huffman_code(huffman_boom) # Hier wordt het omgezet in een dictionary vorm, zodat we meer controle hebben over de getallen en makkelijker het kunnen toepassen
    binaire_getallen = tekst_naar_binair(tekst, huffman_code) # Als er geen str ervoor is, krijgen we error bij de functie 'toegevoegde_waarde_berekenen'
    toegevoegde_waarde =  toegevoegde_waarde_berekenen(binaire_getallen)
    byte_lijst = bouw_byte_lijst(toegevoegde_waarde)
    # for letter, code in sorted(huffman_code.items()):# Nu moeten we nog het in een wat meer leesbare vorm zitten
    #     print(f"{letter} : {code}")
    # b'\x01\x17\xff\xfe' # b'\x01\x17\xff\xfe'
    laatste_bytes= bytes(byte_lijst) # bytes() wordt gebruikt om de lijst met bytes waardes (dat nu nog decimaal is) om te zetten naar bytes objecten
    # https://www.w3schools.com/python/ref_func_bytes.asp#:~:tekst=The%20bytes()%20function%20returns,object%20that%20can%20be%20modified.
    compressed_file = compressie(laatste_bytes, huffman_code)
    a_of_h = auto_of_hand()
    if a_of_h == 'automatisch':
        decompressie(compressed_file, huffman_code)
    elif a_of_h == 'handmatig':
        handmatig_decomprimeren()

pad = test_input() 
if __name__ == "__main__": 
    main()
input('Druk een knop om af te sluiten')
