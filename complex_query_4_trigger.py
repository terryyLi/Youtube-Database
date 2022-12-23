#-----------------------------------------------------------------
# Working with psycopg2
#-----------------------------------------------------------------

import psycopg2
import sys

def heading(str):
    print('-'*60)
    print("** %s:" % (str,))
    print('-'*60, '\n')    

SHOW_CMD = True
def print_cmd(cmd):
    if SHOW_CMD:
        print(cmd.decode('utf-8'))

def print_rows(rows):
    for row in rows:
        print(row)

#------------------------------------------------------------
# show_menu
#------------------------------------------------------------

def show_menu():
    menu = '''

--------------------------------------------------
As a viewer I want to subscribe to different youtube channels so that I can be see my favorite content creators post 

Choose (1, 0 to quit): '''

    try:
        choice = int(input( menu ))
    except ValueError:
        print("\n\n* Invalid choice. Choose again.")
        show_menu()
    else:
        if choice == 0:
            print('Done.')
            cur.close()
            conn.close()
        elif choice in range(1,1+1):
            print()
            actions[choice]()
            show_menu()
        else:
            print("\n\n* Invalid choice (%s). Choose again." % choice)
            show_menu()
    finally:
        if cur != None:
            cur.close() 
        if conn != None:
            conn.close() 

#------------------------------------------------------------
# List demography of who viewed my videos
#------------------------------------------------------------
def update_Verification_menu():
    heading('As a viewer I want to subscribe to different youtube channels so that I can be see my favorite content creators post \n Our assumption based off the size of our data is that a creator will be verified if they have a channel with more than 2 subscribers. \n Enter a viewer name and channel name to subscribe that user to the specified channel:')
    viewer_name = input('Viewer name: ')
    channel_name = input('Channel name: ')
    heading('Below is the creator and subscribing tables:')
    showTableCreator()
    showTableSubscribing()
    update_Verification(viewer_name, channel_name)
    heading('Below is the creator and subscribing tables:')
    showTableCreator()
    showTableSubscribing()

def showTableCreator():
    query = '''
    SELECT *
    FROM creator
    '''
    cmd = cur.mogrify(query)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

def showTableSubscribing():
    query = '''
    SELECT *
    FROM subscribing
    '''
    cmd = cur.mogrify(query)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

def  update_Verification(viewer_name, channel_name):
    query = '''
    CREATE OR REPLACE FUNCTION fn_verify_creator() 
    RETURNS trigger 
    LANGUAGE plpgsql AS 
    $$
    DECLARE creator_id integer := (SELECT user_id FROM Channel  WHERE channel_id = new.channel_id) ;
    BEGIN
    IF (
        (SELECT COUNT(user_id) 
        FROM Subscribing 
        WHERE channel_id = new.channel_id) 
        >= 2) THEN
        UPDATE   creator 
            SET   isVerified = True 
          WHERE   user_id = creator_id;
    END IF;

    return NULL;
    END
    $$;

    DROP TRIGGER IF EXISTS tr_update_verification ON subscribing; 

    CREATE TRIGGER tr_update_verification 
    AFTER INSERT ON subscribing
    FOR EACH ROW
    EXECUTE FUNCTION fn_verify_creator();

    INSERT INTO Subscribing
         VALUES((SELECT user_id FROM Viewer where name = %s), (SELECT channel_id FROM Channel where name = %s));
 
  
    '''
    cmd = cur.mogrify(query, (viewer_name, channel_name))
    print_cmd(cmd)
    cur.execute(cmd)
    # rows = cur.fetchall()
    # print_rows(rows)
    # print()
    # for row in rows:
    #     sum = row
    #     print("%s" % (sum))

# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:  update_Verification_menu}

if __name__ == '__main__':
    try:
        # default database and user
        db, user = 'youtube', 'isdb'
        # you may have to adjust the user 
        # python a4-socnet-sraja.py a4_socnet postgres
        if len(sys.argv) >= 2:
            db = sys.argv[1]
        if len(sys.argv) >= 3:
            user = sys.argv[2]
        # by assigning to conn and cur here they become
        # global variables.  Hence they are not passed
        # into the various SQL interface functions
        conn = psycopg2.connect(database=db, user=user)
        conn.autocommit = True
        cur = conn.cursor()
        show_menu()
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))