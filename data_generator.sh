#! /bin/bash

# usage: ./data_generator.sh -u 15 -e 9 -n 100 -b

helpFunction()
{
   echo ""
   echo "Welcome to mids 205 Project 3 synthetic data generator"
   echo "Usage: $0 -u NOOFUSERS -e ENDPOINTS -n GENERATEREQS"
   echo -e "\t-u Number of users"
   echo -e "\t-e Number of endpoints"
   echo -e "\t-n Number of total requests"
   echo -e "\t-b (Optional) use Apache Bench to send the requests to flask, uses no args just the flag"
   exit 1 # Exit script after printing help
}

while getopts "u:e:n:b" opt
do
   case "$opt" in
      u ) NOOFUSERS="$OPTARG" ;;
      e ) ENDPOINTS="$OPTARG" ;;
      n ) GENERATEREQS="$OPTARG" ;;
      b ) ABFLAG="SET" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$NOOFUSERS" ] || [ -z "$ENDPOINTS" ] || [ -z "$GENERATEREQS" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi


## ** Set limits to per user items
REQS=0
MAXNOOFSWORDS=10 # Max swords purchased at a time per user
MAXNOOFSHIELDS=5 # max shields purchased at a time per user
MAXNOOFPOTIONS=100 # max potions purchased at a time per user
MAXTAKEPOTIONS=3 # max potions taken at a time per user
MAXGUILDS=3 # max number of guilds joined at a time per user
CONCURRENTUSERS=1 #max users accessing the flask API (* Cannot use concurrency level greater than total number of requests [CONCURRENTUSERS < GENERATEREQS] )

## Event Types will be randomly assigned to a number between 1 and 9 based on endpoints specified.
# 1) Purchase a Sword
# 2) Purchase a Shield
# 3) Purchase a Potion
# 4) Find Treasure
# 5) Enemy Attack
# 6) Defeat Enemy
# 7) Take Potion
# 8) Level Up
# 9) Join a Guild - this randomly generate 1 of three guild names Game of Thrones, Castle of Rock, and Knights of the Round table

## ** Check if apache bench optional param is passed 
if [ "$ABFLAG" ]
then
    echo "Apache Bench flag is $ABFLAG";
    # docker exec -it project-3-elizkhan_mids_1 ab -n 2 -H "Host: liz.comcast.com" 'http://localhost:5000/purchase_a_potion/?userid=002&n=10' ## works
    # docker-compose exec mids ab -n 2 -H "Host: liz.comcast.com" http://localhost:5000/ #does not work in windows
    until [ $REQS -gt $GENERATEREQS ]; do
        ID=$(( ( RANDOM % $NOOFUSERS )  + 1 ))
        EP=$(( ( RANDOM % $ENDPOINTS )  + 1 ))
        NOOFSWORDS=$(( ( RANDOM % $MAXNOOFSWORDS )  + 1 ))
        NOOFSHIELDS=$(( ( RANDOM % $MAXNOOFSHIELDS )  + 1 ))
        NOOFPOTIONS=$(( ( RANDOM % $MAXNOOFPOTIONS )  + 1 ))
        TAKENPOTIONS=$(( ( RANDOM % $MAXTAKEPOTIONS )  + 1 ))
        case $EP in
            1)
            docker exec -it project-3-elizkhan_mids_1 ab -n 1 -c $CONCURRENTUSERS -H "Host: user-00$ID.comcast.com" "http://localhost:5000/purchase_a_sword/?userid=%27user-00$ID%27&n="$NOOFSWORDS
            ;;
        esac
        case $EP in
            2)
            docker exec -it project-3-elizkhan_mids_1 ab -n 1 -c $CONCURRENTUSERS -H "Host: user-00$ID.comcast.com" "http://localhost:5000/purchase_a_shield/?userid=%27user-00$ID%27&n="$NOOFSHIELDS
            ;;
        esac
        case $EP in
            3)
            docker exec -it project-3-elizkhan_mids_1 ab -n 1 -c $CONCURRENTUSERS -H "Host: user-00$ID.comcast.com" "http://localhost:5000/purchase_a_potion/?userid=%27user-00$ID%27&n="$NOOFPOTIONS
            ;;
        esac    
        case $EP in
            4)
            docker exec -it project-3-elizkhan_mids_1 ab -n 1 -c $CONCURRENTUSERS -H "Host: user-00$ID.comcast.com" "http://localhost:5000/find_treasure/?userid=%27user-00$ID%27"
            ;;
        esac
        case $EP in
            5)
            docker exec -it project-3-elizkhan_mids_1 ab -n 1 -c $CONCURRENTUSERS -H "Host: user-00$ID.comcast.com" "http://localhost:5000/enemy_attack/?userid=%27user-00$ID%27"
            ;;
        esac
        case $EP in
            6)
            docker exec -it project-3-elizkhan_mids_1 ab -n 1 -c $CONCURRENTUSERS -H "Host: user-00$ID.comcast.com" "http://localhost:5000/defeat_enemy/?userid=%27user-00$ID%27"
            ;;
        esac
        case $EP in
            7)
            docker exec -it project-3-elizkhan_mids_1 ab -n 1 -c $CONCURRENTUSERS -H "Host: user-00$ID.comcast.com" "http://localhost:5000/take_potion/?userid=%27user-00$ID%27&n="$TAKENPOTIONS
            ;;
        esac
        case $EP in
            8)
            docker exec -it project-3-elizkhan_mids_1 ab -n 1 -c $CONCURRENTUSERS -H "Host: user-00$ID.comcast.com" "http://localhost:5000/level_up/?userid=%27user-00$ID%27"
            ;;
        esac
        case $EP in
            9)
              GUILDID=$(( ( RANDOM % $MAXGUILDS )  + 1 ))
              case $GUILDID in
                1)
                docker exec -it project-3-elizkhan_mids_1 ab -n 1 -c $CONCURRENTUSERS -H "Host: user-00$ID.comcast.com" "http://localhost:5000/join_guild/?userid=%27user-00$ID%27"
                ;;
                2)
                docker exec -it project-3-elizkhan_mids_1 ab -n 1 -c $CONCURRENTUSERS -H "Host: user-00$ID.comcast.com" "http://localhost:5000/join_guild/?userid=%27user-00$ID%27&guild_name=%27Game%20of%20Thrones%27"
                ;;
                3)
                docker exec -it project-3-elizkhan_mids_1 ab -n 1 -c $CONCURRENTUSERS -H "Host: user-00$ID.comcast.com" "http://localhost:5000/join_guild/?userid=%27user-00$ID%27&guild_name=%27Castle%20of%20Rock%27"
                ;;
              esac
        esac
        let REQS=REQS+1
    done
else
    until [ $REQS -gt $GENERATEREQS ]; do
        ID=$(( ( RANDOM % $NOOFUSERS )  + 1 ))
        EP=$(( ( RANDOM % $ENDPOINTS )  + 1 ))
        NOOFSWORDS=$(( ( RANDOM % $MAXNOOFSWORDS )  + 1 ))
        NOOFSHIELDS=$(( ( RANDOM % $MAXNOOFSHIELDS )  + 1 ))
        NOOFPOTIONS=$(( ( RANDOM % $MAXNOOFPOTIONS )  + 1 ))
        TAKENPOTIONS=$(( ( RANDOM % $MAXTAKEPOTIONS )  + 1 ))
        case $EP in
            1)
            docker-compose exec mids curl "http://localhost:5000/purchase_a_sword/?userid=%27user-00$ID%27&n="$NOOFSWORDS
            ;;
        esac
        case $EP in
            2)
            docker-compose exec mids curl "http://localhost:5000/purchase_a_shield/?userid=%27user-00$ID%27&n="$NOOFSHIELDS
            ;;
        esac
        case $EP in
            3)
            docker-compose exec mids curl "http://localhost:5000/purchase_a_potion/?userid=%27user-00$ID%27&n="$NOOFPOTIONS
            ;;
        esac
        case $EP in
            4)
            docker-compose exec mids curl "http://localhost:5000/find_treasure/?userid=%27user-00$ID%27"
            ;;
        esac
        case $EP in
            5)
            docker-compose exec mids curl "http://localhost:5000/enemy_attack/?userid=%27user-00$ID%27"
            ;;
        esac
        case $EP in
            6)
            docker-compose exec mids curl "http://localhost:5000/defeat_enemy/?userid=%27user-00$ID%27"
            ;;
        esac
        case $EP in
            7)
            docker-compose exec mids curl "Host: user-00$ID.comcast.com" "http://localhost:5000/take_potion/?userid=%27user-00$ID%27&n="$TAKENPOTIONS
            ;;
        esac
        case $EP in
            8)
            docker-compose exec mids curl "http://localhost:5000/level_up/?userid=%27user-00$ID%27"
            ;;
        esac
        case $EP in
            9)
              GUILDID=$(( ( RANDOM % $MAXGUILDS )  + 1 ))
              case $GUILDID in
                1)
                docker-compose exec mids curl "Host: user-00$ID.comcast.com" "http://localhost:5000/join_guild/?userid=%27user-00$ID%27"
                ;;
                2)
                docker-compose exec mids curl "Host: user-00$ID.comcast.com" "http://localhost:5000/join_guild/?userid=%27user-00$ID%27&guild_name='Game of Thrones'"
                ;;
                3)
                docker-compose exec mids curl "Host: user-00$ID.comcast.com" "http://localhost:5000/join_guild/?userid=%27user-00$ID%27&guild_name='Castle of Rock'"
                ;;
              esac
        esac
        let REQS=REQS+1
    done
fi
