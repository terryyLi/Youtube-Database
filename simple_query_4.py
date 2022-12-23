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
As a viewer I want to be able to comment on videos so that I can ask questions and discuss things I am interested in


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
def insert_comment_menu():
    heading('As a viewer I want to be able to comment on videos so that I can ask questions and discuss things I am interested in \n Enter the comment, viewer name, and video name to comment on a video:')
    # comment_id = input('Comment id (> 500): ')
    content = input('Content: ')
    user_id = input('Viewer name: ')
    video_id = input('Video name: ')
    heading('Below is the comment table:')
    showTable()
    insert_comment( content, user_id, video_id)
    heading('Below is the comment table:')
    showTable()

def showTable():
    query = '''
    SELECT *
    FROM comment
    '''
    cmd = cur.mogrify(query)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

def insert_comment( content, user_id,video_id):
    query = '''
    INSERT INTO Comment
         VALUES((SELECT max(comment_id)+1 FROM Comment), %s, (SELECT user_id FROM Viewer where name = %s) , (SELECT video_id FROM Video where name = %s));
    '''
    cmd = cur.mogrify(query, ( content, user_id, video_id))
    print_cmd(cmd)
    cur.execute(cmd)
    # rows = cur.fetchall()
    # print_rows(rows)
    # print()
    # for row in rows:
    #     user_id, name, gender, age = row
    #     print("%s. %s, %s (%s)" % (user_id, name, gender, age))

# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1: insert_comment_menu}

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


