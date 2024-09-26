from bs4 import BeautifulSoup

def process_file(file):
    with open(file, 'r') as input:
        content = input.read()
    input_soup = BeautifulSoup(content, 'xml') 
    
    #for ct in input_soup.find_all('common-timeline'):
        ##### FAR FROM FINISHED #####

    for tier in input_soup.find_all('tier'): # find all the tiers
        # print("Tier id is: ",tier['id'])
        events_to_merge = [] # list of events to merge
        event = tier.event # iterator for the nexts events to add to the list

        while event: # check if the event in none and THEN if there is a next sibling
            events_to_merge.append(event)
            while 'TT' in event.text: # check if the event has TT in the text (maybe raise error if is just a comma or a space)
                while event.next_sibling and event.next_sibling.name != 'event': ## with the next sibling you get also spaces, commas and \n
                    event.next_sibling.extract() # remove in case is not an event
                if event.next_sibling: # check if the event has a next sibling
                    events_to_merge.append(event.next_sibling)
                event = event.next_sibling
                event.previous_sibling.extract()
            if len(events_to_merge) > 1: # just to avois to call merge_events with just one element in elements_to_merge
                merged_event = merge_events(events_to_merge)
                event = event.next_sibling
                event.previous_sibling.replace_with(merged_event)
                event = event.previous_sibling
            events_to_merge = []
            while event.next_sibling and event.next_sibling.name != 'event': ## with the next sibling you get also spaces, commas and \n
                event.next_sibling.extract()
            event = event.next_sibling
        print("\n\n\n")

        for event in tier.find_all('event'):
            event.insert_after(BeautifulSoup('\n', 'html.parser'))

    return str(input_soup)


def merge_events(events: list):
    # print("Events to merge: ",events)
    first_event = events[0]
    last_event = events[-1]
    # print("first ebent",first_event)
    # print("LAST ebent",last_event)
    start = first_event['start']
    # print(start)
    end = last_event['end']
    # print(end)
    text = ''
    for event in events:
        text += remove_tt(event.text)
        if event != last_event:
            text += ' '
    merged_event = BeautifulSoup('<event start="{}" end="{}">{}</event>'.format(start, end, text), 'html.parser')
    return merged_event

def remove_tt(text):
    # this funxtion has to remove also some space near TT if there are any
    # as of now is kinda stupid
    return text.replace('TT', '')
    """if text.find('TT') == -1:
        return text
    else :
        if text.find(' TT') != -1:
            return text.replace(' TT', '')
        elif text.find('TT ') != -1:
            return text.replace('TT ', '')
        else:
            return text.replace('TT', '')"""
            
    
        
# save the changes to a new file
def save_file(file, content):
    with open(file, 'w') as output:
        output.write(content)





def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()

    if content1 == content2:
        print("The files are equal.")
    else:
        print("The files are not equal.")


def compare_files_tiers(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()
    soup1 = BeautifulSoup(content1, 'xml')
    soup2 = BeautifulSoup(content2, 'xml')

    tiers1 = soup1.find_all('tier')
    tiers2 = soup2.find_all('tier')

    check = 0
    if len(tiers1) == len(tiers2):
        # print("i due file hanno lo stesso numero di tier")
        for i in range(len(tiers1)):
            
            tier1 = tiers1[i]
            tier2 = tiers2[i]
            # print(tier1)
            # print(tier2)
            if tier1.attrs == tier2.attrs:
                for tier1_event, tier2_event in zip(tier1.find_all('event'), tier2.find_all('event')):
                    if tier1_event.attrs == tier2_event.attrs and tier1_event.text == tier2_event.text:
                        continue
                    else:
                        # print("gli eventi sono diversi")
                        # print("\n\n", tier1_event, "\n\n", tier2_event, "\n\n")
                        check +=1
                    #print("Counter: ", counter)
                continue
            else:
                check += 1
                #print("il tier ", i, " è diverso")
                #print("\n\n", tier1, "\n\n", tier2, "\n\n")
        
    else:
        #print("Neanche lo stesso numero di tier")
        check += 1
    
    if check == 0:
        print("\t[tier_check]I file sono uguali, controllando solo i tier")
    else:
        print("\t[tier_check]I file sono diversi", check)

def main():
    input = 'exercise_1/in_example.exb'
    true_output = 'exercise_1/out_example.exb'
    output = 'exercise_1/my_out_example.exb'

    print("[main] Processing del file di input...")
    content = process_file(input)
    print("[main] Processing completato.")
    print("[main] Salvataggio dell'output...")
    save_file(output, content)
    print("[main] Salvataggio completato.")

    print("[main] Confronto tra i tier del file di output e quello di riferimento...")
    compare_files_tiers(true_output, output)

if __name__ == "__main__":
    main()


