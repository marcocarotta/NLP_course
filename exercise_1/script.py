from bs4 import BeautifulSoup

def process_file(file):
    with open(file, 'r') as input:
        content = input.read()
    input_soup = BeautifulSoup(content, 'xml') 
    
    #for ct in input_soup.find_all('common-timeline'):
        ##### FAR FROM FINISHED #####

    for tier in input_soup.find_all('tier'): # find all the tiers
        print("Tier id is: ",tier['id'])
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
                """event.insert_after(merged_event)
                event = event.next_sibling
                event.next_sibling.extract()"""
            events_to_merge = []
            while event.next_sibling and event.next_sibling.name != 'event': ## with the next sibling you get also spaces, commas and \n
                event.next_sibling.extract()
            event = event.next_sibling
        print("\n\n\n")

    return input_soup.prettify()
    

        

"""         for event in tier.children:
            if 'TT' in event.text:
                # print(event.text)
                # counter += 1
                events_to_merge.append(event)
            else:
                events_to_merge.append(event)
                if len(events_to_merge) > 1:
                    merged_event = merge_events(events_to_merge)
                    for e in events_to_merge:
                        tier.e.extract()
                    tier.append(merged_event) """


    # Process the content here

def merge_events(events: list):
    print("Events to merge: ",events)
    first_event = events[0]
    last_event = events[-1]
    print("first ebent",first_event)
    print("LAST ebent",last_event)
    start = first_event['start']
    print(start)
    end = last_event['end']
    print(end)
    text = ''
    for event in events:
        """start = event['start']
        end = event['end']
        if start < min_start:
            min_start = start
        if end > max_end:
            max_end = end """
        text += remove_tt(event.text)
    merged_event = BeautifulSoup('<event start="{}" end="{}">{}</event>'.format(start, end, text), 'html.parser')
    return merged_event

def remove_tt(text):
    return text.replace('TT', '')
        
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



def main():
    input = 'exercise_1/in_example.exb'
    true_output = 'exercise_1/out_example.exb'
    output = 'exercise_1/my_out_example.exb'

    content = process_file(input)
    print("[main] Salvataggio dell'output...")
    save_file(output, content)
    #compare_files(file1, file2)

if __name__ == "__main__":
    main()


"""def process_file(file):
    with open(file, 'r') as input:
        content = input.read()
    input_soup = BeautifulSoup(content, 'xml') 
    
    #for ct in input_soup.find_all('common-timeline'):
        ##### FAR FROM FINISHED #####

    for tier in input_soup.find_all('tier'): # find all the tiers
        print("Tier id is: ",tier['id'])
        events_to_merge = [] # list of events to merge
        
        # current_event = tier.event # first event of the list
        event = tier.event # iterator for the nexts events to add to the list
        while event: # check if the event in none and THEN if there is a next sibling
            print("PRIMO WHILE")
            events_to_merge.append(event)
            while event and 'TT' in event.text: # check if the event in none and THEN check if the event is a TT event (lazy checking?)
                #print("secondo WHILE")
                while event.next_sibling and event.next_sibling.name != 'event': ## with the next sibling you get also spaces, commas and \n
                    event.next_sibling.extract()
                    #print("Terzo1 WHILE")

                print("COSA METTO QUI DENTRO:",event.next_sibling)
                events_to_merge.append(event.next_sibling)
                event = event.next_sibling
                event.previous_sibling.extract()
                merged_event = merge_events(events_to_merge)
                event.replace_with(merged_event)
                print("MERGED EVENT",merged_event)
                print("NEXT EVENT",event)
                while event.next_sibling and event.next_sibling.name != 'event': ## with the next sibling you get also spaces, commas and \n
                    event.next_sibling.extract()
                    #print("Terzo2 WHILE")
                if event.next_sibling: event = event.next_sibling
                else: break 
            events_to_merge = []

            print("NEXT EVENT NOW IS:",event)

            while event.next_sibling and event.next_sibling.name != 'event': ## with the next sibling you get also spaces, commas and \n
                event.next_sibling.extract()
                #print("Terzo3 WHILE")
            if event.next_sibling: event = event.next_sibling
            else: break
            
            print("NEXT EVENT NOW IS:",event)

    print("\n\n\n")
    return input_soup.prettify()"""