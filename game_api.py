#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')

"""[summary]

Returns:
    [type]: [description]
"""

def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())

@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"

"""Purchase a sword
usage: GET http://localhost:5000/purchase_a_sword/?userid=%27002%27&n=3
Returns:
    [type]: [description]
"""
@app.route("/purchase_a_sword/", methods=['POST','GET'])
def purchase_a_sword():
    """
    @function: This function generate a Purchase a Sword event from a user mobile device request or Apache Bench
    @param: User Request (via URL endpoint) 
    @return: Returns string of User Id and Event 
    """
    userid = request.args.get('userid', default='001', type=str)
    n = request.args.get('n',default=1,type=int)
    purchase_sword_event = {'userid': userid,
                            'event_type': 'purchase_sword',
                            'item_type': 'sword',
                            'description': 'very sharp steel sword',
                            'amount_purchased': n,
                            'price' : 100}
    log_to_kafka('events', purchase_sword_event)
    return "USER " + userid + ": "+ str(n)+" "+ " Sword(s) Purchased!\n"



"""Join a Guild
usage: GET http://localhost:5000/join_guild/?userid=%27002%27&guild_name=%27Elizabeth%20Khan%27'

Returns:
    [type]: [description]
"""
@app.route("/join_guild/", methods=['POST','GET'])
def join_guild():
    """
    @function: This function generate a Join Guild event from a user mobile device request or Apache Bench
    @param: User Request (via URL endpoint) 
    @return: Returns string of User Id and Event 
    """
    userid = request.args.get('userid', default='001', type=str)
    guild_name = request.args.get('guild_name',default="Knights of the Round Table",type=str)
    join_guild_event = {'userid': userid,
                        'event_type': 'join_guild',
                        'description': 'a very large guild',
                        'guild_name': guild_name }
    log_to_kafka('events', join_guild_event)
    return "Joined" +" "+ guild_name +" "+ "Guild!\n"
    
    #TODO: 
    # Add userid in your return
    # Add doc string  
        
        
"""Purchase a shield
usage: GET http://localhost:5000/purchase_a_shield/?userid=%27002%27&n=3
Returns:
    [type]: [description]
"""
@app.route("/purchase_a_shield/", methods=['POST','GET'])
def purchase_a_shield():
    """
    @function: This function generate a Purchase a Shield event from a user mobile device request or Apache Bench
    @param: User Request (via URL endpoint) 
    @return: Returns string of User Id and Event 
    """
    userid = request.args.get('userid', default='001', type=str)
    n = request.args.get('n',default=1,type=int)
    purchase_shield_event = {'userid': userid,
                             'event_type': 'purchase_shield', 
                             'item_type': 'shield',
                             'description': 'very solid protective shield',
                             'amount_purchased': n,
                             'price': 50}
    log_to_kafka('events', purchase_shield_event)
    return str(n) + " " + " Shield(s) Purchased!\n"
    #TODO: 
    # Add userid in your return
    # Add doc string  
    

"""Purchase a potion
Usage: GET http://localhost:5000/purchase_a_potion/?userid=%27002%27&n=3
Returns:
    [type]: [description]
"""

@app.route("/purchase_a_potion/", methods=['POST','GET'])
def purchase_a_potion():
    """
    @function: This function generate a Purchase Potion event from a user mobile device request or Apache Bench
    @param: User Request (via URL endpoint) 
    @return: Returns string of User Id and Event 
    """
    userid = request.args.get('userid', default='001', type=str)
    n = request.args.get('n',default=1,type=int)
    purchase_shield_event = {'userid': userid,
                             'event_type': 'purchase_potion',
                             'item_type': 'potion',
                             'description': 'mystical potion with healing powers',
                             'amount_purchased': n,
                             'price': 5}
    log_to_kafka('events', purchase_shield_event)
    return "USER " + userid + ": "+ str(n)+" "+ " Potion(s) Purchased!\n"
    
    
    
"""Find treasure
Usage: GET http://localhost:5000/find_treasure/?userid=%27002%27
Returns:
    [type]: [description]
"""    
@app.route("/find_treasure/")
def find_treasure():
    """
    @function: This function generate a Find Treasure event from a user mobile device request or Apache Bench
    @param: User Request (via URL endpoint) 
    @return: Returns string of User Id and Event 
    """
    userid = request.args.get('userid', default='001', type=str)
    find_treasure_event = {'userid': userid,
                           'event_type': 'find_treasure',
                           'description': 'a small treasure chest of jewels and gold'}
    log_to_kafka('events', find_treasure_event)
    return "USER " + userid + ": " + "Treasure Found!\n"  
    
 
"""Enemy attacked
Usage: GET http://localhost:5000/enemy_attack/?userid=%27002%27
Returns:
    [type]: [description]
"""     
@app.route("/enemy_attack/")
def enemy_attack():
    """
    @function: This function generate an Enemy Attack event from a user mobile device request or Apache Bench
    @param: User Request (via URL endpoint) 
    @return: Returns string of User Id and Event 
    """
    userid = request.args.get('userid', default='001', type=str)
    find_treasure_event = {'userid': userid,
                           'event_type': 'enemy_attack',
                           'description': 'an enemy suprise attack reduces health'}
    log_to_kafka('events', find_treasure_event)
    return "USER " + userid + ": " + "An enemy attacked!\n" 


"""Enemy attacked
Usage: GET http://localhost:5000/defeat_enemy/?userid=%27002%27
Returns:
    [type]: [description]
"""  
@app.route("/defeat_enemy/")
def defeat_enemy():
    """
    @function: This function generate an Defeat Enemy event from a user mobile device request or Apache Bench
    @param: User Request (via URL endpoint) 
    @return: Returns string of User Id and Event 
    """
    userid = request.args.get('userid', default='001', type=str)
    defeat_enemy_event = {'userid': userid,
                          'event_type': 'defeat_enemy',
                          'description': 'the enemy lost the battle'}
    log_to_kafka('events', defeat_enemy_event)
    return userid + ": " + "Enemy defeated!\n"     

"""Take potions
Usage: GET http://localhost:5000/take_potion/?userid=%27002%27&n=3
Returns:
    [type]: [description]
"""  

@app.route("/take_potion/", methods=['POST','GET']) 
def take_potion():
    """
    @function: This function generate a Take Potion event from a user mobile device request or Apache Bench
    @param: User Request (via URL endpoint) 
    @return: Returns string of User Id and Event 
    """
    userid = request.args.get('userid', default='001', type=str)
    n = request.args.get('n',default=1,type=int)
    take_potion_event = {'userid': userid,
                         'event_type': 'take_potion',
                         'description': 'potion returned some health points',
                         'level': 0,
                         'attack': 0,
                         'defense': 0,
                         'health': 10*n}
    log_to_kafka('events', take_potion_event)
    return "USER " + userid + ": " + str(n) +" "+ " Potion(s) Used!\n"
 

"""Take potions
Usage: GET http://localhost:5000/level_up/?userid=%27002%27
Returns:
    [type]: [description]
"""  

@app.route("/level_up/") 
def level_up():
    """
    @function: This function generate a Level Up event from a user mobile device request or Apache Bench
    @param: User Request (via URL endpoint) 
    @return: Returns string of User Id and Event 
    """
    userid = request.args.get('userid', default='001', type=str)
    level_up_event = {'userid': userid,
                      'event_type': 'level_up',
                      'description': 'an increase in player level, attack, and defense',
                      'level': 1,
                      'attack': 200,
                      'defense': 175,
                      'health': 100}
    log_to_kafka('events', level_up_event)
    return "USER " + userid + ": " + "Leveled Up!\n"