import android
import random
import sqlite3

droid = android.Android()
#/storage/sdcard/sl4a/scripts/
conn = sqlite3.connect('shuffleWord.db')
cur = conn.cursor()

conn.execute('CREATE TABLE if not exists shuffleWord (shuf_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, foodIns TEXT NOT NULL)')

# //---------- S T A R T  F U N C T I O N S ----------//

# -- START FUNCTION ADD WORD --
def AddWordFood():
    dict = droid.fullQueryDetail("addFood").result
    foodInsert = dict['text']
    if foodInsert != "":
        try:
            inFood = foodInsert.upper()
            conn = sqlite3.connect("shuffleWord.db")
            cur = conn.execute("SELECT count(*) FROM shuffleWord WHERE foodIns = '"+inFood+"' ")
            if cur.fetchone()[0]:
                droid.makeToast("Food '"+ foodInsert + "' already exist!")
                droid.fullSetProperty("buttonAdd2","background","#00cc7a")
                droid.fullSetProperty("addFood","text","")
            else:
                conn.execute("INSERT INTO shuffleWord (foodIns)VALUES('"+inFood+"')")
                conn.commit()
                droid.makeToast("Food '"+ foodInsert +"' is successfully added!")
                droid.fullSetProperty("addFood","text","")
                droid.fullSetProperty("buttonAdd2","background","#00cc7a")
                
        except sqlite3.Error as e:
            droid.dialogCreateAlert("Error", "Error in saving!",e)
            droid.fullSetProperty("buttonAdd2","background","#00cc7a")
        finally:
            if conn:
                conn.close()
    else:
        droid.fullSetProperty("buttonAdd2","background","#00cc7a")
        droid.makeToast("Please fill the field!")
    
# -- END FUNCTION ADD WORD --

# -- START FUNCTION RANDOM FOOD --
def randomFunction():
    global randomFood
    randomFood = ''
    conn = sqlite3.connect("shuffleWord.db")
    cur = conn.execute("SELECT foodIns FROM shuffleWord")
    wordList = []
    for row in cur:
        wordList.append(row[0])
    if len(wordList) > 0:
        droid.fullSetProperty("showFood","text",random.choice(wordList)) 
# -- END FUNCTION RANDOM FOOD --

# -- START FUNCTION VIEW LIST OF FOOD --
def ListFood():
    conn = sqlite3.connect("shuffleWord.db")
    cur = conn.execute("SELECT foodIns FROM shuffleWord")
    foodList = []
    for row in cur:
        foodList.append(row[0])
    conn.close()
    if len(foodList) > 0:
        droid.dialogCreateAlert("Food List")
        droid.dialogSetItems(foodList)
        droid.dialogSetNegativeButtonText('Back')
        droid.dialogShow()
    
# -- END FUNCTION VIEW LIST OF FOOD --

# -- START FUNCTION TO EDIT FOOD --
def toEditFood():
    foodName = f
    conn = sqlite3.connect("shuffleWord.db")
    cur = conn.execute("SELECT * FROM shuffleWord WHERE foodIns='"+foodName+"' ")
    rslt = list(cur)
    global FOODID
    FOODID = ''
    FOODID = str(rslt[0][0])
    droid.fullSetProperty("updateFood","text",foodName)
    conn.close()
# -- END FUNCTION TO EDIT FOOD --

# -- START FUNCTION UPDATE FOOD --
def toUpdateFood():
    dict = droid.fullQueryDetail("updateFood").result
    foodUpdate = dict['text']
    try:
        upFood = foodUpdate.upper()
        conn = sqlite3.connect("shuffleWord.db")
        cur = conn.execute("UPDATE shuffleWord SET foodIns = '"+upFood+"' WHERE shuf_id = '"+FOODID+"' ")
        conn.commit()
        droid.makeToast("Food '"+ upFood +"' is successfully updated!")
        droid.fullSetProperty("buttonList","background","#4d88ff")
        settingsLayout()
    except sqlite3.Error as e:
        droid.makeToast("Error in Updating!",e)
    finally:
        if conn:
            conn.close()
# -- END FUNCTION UPDATE FOOD --

# -- START FUNCTION DELETE FOOD --
def toDeleteFood():
    droid.dialogCreateAlert("Action","Are you sure you want to delete?")
    droid.dialogSetPositiveButtonText("YES")
    droid.dialogSetNegativeButtonText("NO")
    droid.dialogShow()

    response = droid.dialogGetResponse().result

    if response["which"] == "positive":
        conn = sqlite3.connect("shuffleWord.db")
        conn.execute("DELETE FROM shuffleWord WHERE shuf_id='"+FOODID+"'")
        conn.commit()
        droid.makeToast("Food successfully Delete!")
        droid.fullSetProperty("buttonList","background","#4d88ff")
        settingsLayout()
# -- END FUNCTION DELETE FOOD --

# //---------- E N D  F U N C T I O N S ----------//


# //---------- S T A R T  E V E N T S ----------//

# -- START EVENT MAIN LAYOUT --
def EventMain():
    i = 0
    while True:
        event = droid.eventWait().result
        print (event)
        response = event["data"]
        if 'data' in event:
            if 'key' in event["data"]:
                result = event["data"]["key"]
        if event["name"] == "screen":
            if event["data"] == "destroy":
                return
            
        elif event["name"] == "key":
            
            if result == "4":
                i = i + 1
                droid.makeToast("Press again to Exit")
                
                if i == 2:
                     droid.fullDismiss()
                     
        elif event["name"] == "click":    
            id = event["data"]["id"]
            
            if id == "buttonReveal":
                global randomFood
                randomFood = ''
                conn = sqlite3.connect("shuffleWord.db")
                
                cur = conn.execute("SELECT foodIns FROM shuffleWord")
                l = len(cur.fetchall())
                 
                wordList = []
                for row in cur:
                    wordList.append(row[0])
                if len(wordList) > 0:
                    randomFood = random.choice(wordList)
                    
                if l == 0:
                    droid.makeToast("No food added.")
                    LayoutMain()
                    
                else:
                    droid.dialogCreateSpinnerProgress()
                    droid.dialogShow()   
                    revealFood()
                    
                conn.close()
                
            elif id == "buttonSettings":
                droid.fullSetProperty("buttonSettings","background","#999")
                settingsLayout()

# -- END EVENT MAIN LAYOUT

# -- START EVENT REVEAL LAYOUT -- 
def EventReveal():
    while True:
        event = droid.eventWait().result
        print (event)
        if 'data' in event:
            if 'key' in event["data"]:
                result = event["data"]["key"]
        if event["name"] == "screen":
            if event["data"] == "destroy":
                return
        elif event["name"] == "key":
             if result == "4":
                LayoutMain()
        elif event["name"] == "click":
            id = event["data"]["id"]
            if id == "buttonBack":
                droid.fullSetProperty("buttonBack","background","#999")
                LayoutMain();
# -- END EVENT REVEAL LAYOUT -- 

# -- START EVENT ADD LAYOUT --
def EventAdd():
    while True:
        event = droid.eventWait().result
        print (event)
        if 'data' in event:
            if 'key' in event["data"]:
                result = event["data"]["key"]
        if event["name"] == "screen":
            if event["data"] == "destroy":
                return
        elif event["name"] == "key":
            if result == "4":
                droid.fullSetProperty("buttonSettings","visibility","visible")
                settingsLayout()
        elif event["name"] == "click":
            id = event["data"]["id"]
            if id == "buttonAdd2":
                droid.fullSetProperty("buttonAdd2","background","#999")
                AddWordFood();
# -- END EVENT ADD LAYOUT --

# -- START EVENT SETTINGS LAYOUT --
def EventSettings():
    while True:
        event = droid.eventWait().result
        print (event)
        if 'data' in event:
            if 'key' in event["data"]:
                result = event["data"]["key"]
        if event["name"] == "screen":
            if event["data"] == "destroy":
                return
        elif event["name"] == "key":
            if result == "4":
                LayoutMain()
        elif event["name"] == "click":
            id = event["data"]["id"]
            if id == "addButton":
                droid.fullSetProperty("addButton","background","#999")
                AddFood();
            if id == "buttonAbout":
                droid.fullSetProperty("buttonAbout","background","#999")
                About()
            if id == "buttonList":
                droid.fullSetProperty("buttonList","background","#999")
                ListFood()
                EventFoodList()
# -- END EVENT SETTINGS LAYOUT --

# -- START EVENT ABOUT LAYOUT --
def EventAbout():
    while True:
        event = droid.eventWait().result
        print (event)
        if 'data' in event:
            if 'key' in event["data"]:
                result = event["data"]["key"]
        if event["name"] == "screen":
            if event["data"] == "destroy":
                return
        elif event["name"] == "key":
            if result == "4":
                settingsLayout()
# -- END EVENT ABOUT LAYOUT --

# -- START EVENT LIST FOOD --
def EventFoodList():
    while True:
        event = droid.eventWait().result
        response = droid.dialogGetResponse().result
        print (event)
        print (response)
        conn = sqlite3.connect("shuffleWord.db")
        cur = conn.execute("SELECT foodIns FROM shuffleWord")
        foodLists = []
        for row in cur:
            foodLists.append(row[0])
        conn.close()
        print (foodLists)
        if 'data' in event:
            if 'key' in event["data"]:
                result = event["data"]["key"]
        if event["name"] == "screen":
            if event["data"] == "destroy":
                return
        elif event["name"] == "key":
            if result == "4":
                droid.fullSetProperty("buttonList","background","#4d88ff")
                settingsLayout()
        elif "which" in response:
            if response["which"] == "negative":
                settingsLayout()
        elif "item" in response:
            global f
            f = ""
            Index = response["item"]
            f = foodLists[Index]
            print (f)
            FoodEdit()
            
# -- END EVENT LIST FOOD --

# -- START EVENT FOOD EDIT --
def EventFoodEdit():
    while True:
        event = droid.eventWait().result
        print (event)
        if 'data' in event:
            if 'key' in event["data"]:
                result = event["data"]["key"]
        if event["name"] == "screen":
            if event["data"] == "destroy":
                return
        elif event["name"] == "key":
            if result == "4":
                settingsLayout()
    #toUpdateFood()
                #buttonUpdate
                #buttonDelete
                #cancelButton
        if event["name"] == "click":
            id = event["data"]["id"]
            if id == "buttonUpdate":
                toUpdateFood()
            elif id == "buttonDelete":
                toDeleteFood()
            elif id == "cancelButton":
                settingsLayout()
# -- END EVENT FOOD EDIT --

# //---------- E N D  E V E N T S ----------//


# //---------- S T A R T  L A Y O U T S ----------//

# -- START ABOUT LAYOUT --
def About():
    aboutLayout = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#009999"
    android:gravity="center|top"
    android:orientation="vertical"
    android:padding="5dp"
    android:visibility="visible"
    tools:context=".ScriptActivity" >

    <LinearLayout
        android:id="@+id/main_linearLayout16"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:baselineAligned="true"
        android:gravity="center"
        android:background="#3366ff"
        android:orientation="vertical"
        android:padding="20dp"
        android:visibility="visible" >

        <TextView
            android:id="@+id/textView9"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Food Trip ðﾟﾍﾔðﾟﾍﾟ"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#ffffff"
            android:textSize="20sp"
            android:textStyle="bold"
            android:typeface="monospace" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/main_linearLayout17"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="30dp"
        android:gravity="center"
        android:orientation="vertical"
        android:padding="10dp" >

        <TextView
            android:id="@+id/textView10"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:paddingBottom="40dp"
            android:textSize="15sp"
            android:textColor="#ffffff"
            android:text="CREATORS:"
            android:textAppearance="?android:attr/textAppearanceMedium" />

	<TextView
	    android:id="@+id/creator1"
	    android:layout_width="wrap_content"
	    android:layout_height="wrap_content"
	    android:textSize="15sp"
	    android:paddingBottom="40dp"
	    android:textColor="#ffffff"
	    android:text="Francis Jay N. Redrino" />

	<TextView
            android:id="@+id/creator2"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textSize="15sp"
            android:textColor="#ffffff"
            android:text="Patricia Pamela P. Pamplona" />
    </LinearLayout>

</LinearLayout>
"""
    print (droid.fullShow(aboutLayout))
    EventAbout()
    droid.fullDismiss()
# -- END ABOUT LAYOUT -- 

# -- START ADDING FOOD LAYOUT --
def AddFood():
    addfoodLayout = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#009999"
    android:gravity="center|top"
    android:orientation="vertical"
    android:padding="5dp"
    android:visibility="visible"
    tools:context=".ScriptActivity" >

    <LinearLayout
        android:id="@+id/main_linearLayout14"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:baselineAligned="true"
        android:gravity="center"
        android:background="#3366ff"
        android:orientation="vertical"
        android:padding="20dp"
        android:visibility="visible" >

        <TextView
            android:id="@+id/textView7"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Food Trip"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#ffffff"
            android:textSize="20sp"
            android:textStyle="bold"
            android:typeface="monospace" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/main_linearLayout15"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="90dp"
        android:gravity="center"
        android:orientation="vertical"
        android:padding="10dp" >

        <TextView
            android:id="@+id/textView8"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Food Name:"
            android:textColor="#ffffff"
            android:textSize="18sp"
            android:textAppearance="?android:attr/textAppearanceMedium" />

        <EditText
            android:id="@+id/addFood"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:ems="10" >

            <requestFocus />
        </EditText>

    </LinearLayout>

    <Button
        android:id="@+id/buttonAdd2"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:background="#00cc7a"
        android:padding="10dp"
        android:text="Add"
        android:width="290dp" />

</LinearLayout>

"""
    print (droid.fullShow(addfoodLayout))
    EventAdd()
    droid.fullDismiss()
# -- END ADDING FOOD LAYOUT -- 
    
# -- START REVEAL FOOD LAYOUT --
def revealFood():
    layoutReveal = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#009999"
    android:gravity="center|top"
    android:orientation="vertical"
    android:padding="5dp"
    android:visibility="visible"
    tools:context=".ScriptActivity" >

    <LinearLayout
        android:id="@+id/main_linearLayout11"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:baselineAligned="true"
        android:gravity="center"
        android:background="#3366ff"
        android:orientation="vertical"
        android:padding="20dp"
        android:visibility="visible" >

        <TextView
            android:id="@+id/textView6"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Food Trip"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#ffffff"
            android:textSize="20sp"
            android:textStyle="bold"
            android:typeface="monospace" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/main_linearLayout12"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="60dp"
        android:gravity="center"
        android:orientation="vertical"
        android:padding="10dp" >

        <EditText
            android:id="@+id/showFood"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:background="#009999"
            android:clickable="false"
            android:ems="10"
            android:focusable="false"
            android:focusableInTouchMode="false"
            android:gravity="center"
            android:inputType="text"
            android:text="Food Here"
            android:textColor="#ffffff"
            android:textSize="16sp"
            android:textStyle="bold"
            android:typeface="normal"
            android:visibility="visible" />

    </LinearLayout>

    <LinearLayout
        android:id="@+id/main_linearLayout13"
        android:layout_width="295dp"
        android:layout_height="wrap_content"
        android:layout_marginRight="10dp"
        android:layout_marginLeft="10dp"
        android:layout_marginTop="100dp"
        android:gravity="center"
        android:orientation="vertical" >

        <Button
            android:id="@+id/buttonBack"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:background="#009999"
            android:padding="30dp"
            android:text="TRY AGAIN"
            android:textColor="#ffffff"
            android:textSize="15sp"
            android:visibility="visible"/>
        
    </LinearLayout>

</LinearLayout>

"""
    print (droid.fullShow(layoutReveal))
    randomFunction()
    droid.dialogDismiss()
    EventReveal()
    droid.fullDismiss()
# -- END REVEAL FOOD LAYOUT --

# -- START VIEW LIST OF FOOD --
def FoodEdit():
    foodEditLayout = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#009999"
    android:gravity="center|top"
    android:orientation="vertical"
    android:padding="5dp"
    android:visibility="visible"
    tools:context=".ScriptActivity" >

    <LinearLayout
        android:id="@+id/main_linearLayout9"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:baselineAligned="true"
        android:gravity="center"
        android:background="#3366ff"
        android:orientation="vertical"
        android:padding="20dp"
        android:visibility="visible" >

        <TextView
            android:id="@+id/textView4"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Food Trip"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#ffffff"
            android:textSize="20sp"
            android:textStyle="bold"
            android:typeface="monospace" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/main_linearLayout10"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="30dp"
        android:gravity="center"
        android:orientation="vertical"
        android:padding="10dp" >

        <TextView
            android:id="@+id/textView5"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Food Name:"
            android:textColor="#ffffff"
            android:textSize="18sp"
            android:textAppearance="?android:attr/textAppearanceMedium" />

        <EditText
            android:id="@+id/updateFood"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:ems="10" >

            <requestFocus />
        </EditText>

    </LinearLayout>

    <Button
        android:id="@+id/buttonUpdate"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:background="#00cc7a"
        android:padding="30dp"
        android:text="Update"
        android:width="290dp" />

    <Button
        android:id="@+id/buttonDelete"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="10dp"
        android:width="290dp"
        android:background="#b30000"
        android:padding="10dp"
        android:text="Delete" />

    <Button
        android:id="@+id/cancelButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_marginTop="30dp"
        android:padding="15dp"
        android:width="290dp"
        android:background="#3366ff"
        android:text="Cancel" />

</LinearLayout>
"""
    print (droid.fullShow(foodEditLayout))
    toEditFood()
    EventFoodEdit()
    droid.fullDismiss()
# -- END VIEW LIST OF FOOD --

# -- START SETTINGS LAYOUT --
def settingsLayout():
    layoutSettings = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#009999"
    android:gravity="center|top"
    android:orientation="vertical"
    android:padding="5dp"
    android:visibility="visible"
    tools:context=".ScriptActivity" >

    <LinearLayout
        android:id="@+id/main_linearLayout7"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:baselineAligned="true"
        android:gravity="center"
        android:background="#3366ff"
        android:orientation="vertical"
        android:padding="20dp"
        android:visibility="visible" >

        <TextView
            android:id="@+id/textView3"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Food Trip"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#ffffff"
            android:textSize="20sp"
            android:textStyle="bold"
            android:typeface="monospace" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/main_linearLayout8"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="40dp"
        android:gravity="center"
        android:orientation="vertical"
        android:padding="10dp" >

        <Button
            android:id="@+id/addButton"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:background="#33ff77"
            android:padding="30dp"
            android:text="Add Food(+)"
            android:width="600dp"/>

        <Button
            android:id="@+id/buttonList"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="5dp"
            android:padding="30dp"
            android:background="#4d88ff"
            android:width="600dp"
            android:text="Food List"/>

        <Button
            android:id="@+id/buttonAbout"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginTop="5dp"
            android:padding="30dp"
            android:background="#b3b300"
            android:width="600dp"
            android:text="About"/>

    </LinearLayout>

</LinearLayout>

"""
    print (droid.fullShow(layoutSettings))
    droid.dialogDismiss()
    EventSettings()
    droid.fullDismiss()
# -- END OF SETTINGS LAYOUT --

# -- START MAIN LAYOUT(CALL) --
def LayoutMain():
    layoutMain = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#009999"
    android:gravity="center|top"
    android:orientation="vertical"
    android:padding="5dp"
    android:visibility="visible"
    tools:context=".ScriptActivity" >

    <LinearLayout
        android:id="@+id/main_linearLayout4"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:baselineAligned="true"
        android:gravity="center"
        android:background="#3366ff"
        android:orientation="vertical"
        android:padding="20dp"
        android:visibility="visible" >

        <TextView
            android:id="@+id/textView2"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Food Trip"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#ffffff"
            android:textSize="20sp"
            android:textStyle="bold"
            android:typeface="monospace" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/main_linearLayout5"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="100dp"
        android:gravity="center"
        android:orientation="vertical"
        android:padding="10dp" >

        <Button
            android:id="@+id/buttonReveal"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:background="#b30000"
            android:padding="20dp"
            android:text="Start"
            android:textColor="#ffffff"
            android:textSize="30sp"
            android:textStyle="bold"
            android:typeface="monospace" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/main_linearLayout6"
        android:layout_width="295dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="110dp"
        android:gravity="center"
        android:orientation="vertical" >

        <Button
            android:id="@+id/buttonSettings"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:background="#009999"
            android:text="Settings"
            android:textColor="#ffffff"
            android:textSize="15sp" />
        
    </LinearLayout>

</LinearLayout>
"""
    print (droid.fullShow(layoutMain))
    EventMain()
    droid.dialogDismiss()
    droid.fullDismiss()
# -- END OF MAIN LAYOUT(CALL) --

# -- START MAIN LAYOUT -- #
layoutMain = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#009999"
    android:gravity="center|top"
    android:orientation="vertical"
    android:padding="5dp"
    android:visibility="visible"
    tools:context=".ScriptActivity" >

    <LinearLayout
        android:id="@+id/main_linearLayout1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:baselineAligned="true"
        android:gravity="center"
        android:background="#3366ff"
        android:orientation="vertical"
        android:padding="20dp"
        android:visibility="visible" >

        <TextView
            android:id="@+id/textView1"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Food Trip"
            android:textAppearance="?android:attr/textAppearanceLarge"
            android:textColor="#ffffff"
            android:textSize="20sp"
            android:textStyle="bold"
            android:typeface="monospace" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/main_linearLayout2"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="100dp"
        android:gravity="center"
        android:orientation="vertical"
        android:padding="10dp" >

        <Button
            android:id="@+id/buttonReveal"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:background="#b30000"
            android:padding="20dp"
            android:text="Start"
            android:textColor="#ffffff"
            android:textSize="30sp"
            android:textStyle="bold"
            android:typeface="monospace" />
    </LinearLayout>

    <LinearLayout
        android:id="@+id/main_linearLayout3"
        android:layout_width="295dp"
        android:layout_height="wrap_content"
        android:layout_marginTop="110dp"
        android:gravity="center"
        android:orientation="vertical" >

        <Button
            android:id="@+id/buttonSettings"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:background="#009999"
            android:padding="20dp"
            android:text="Settings"
            android:textColor="#ffffff"
            android:textSize="15sp"
            android:visibility="visible"/>
        
    </LinearLayout>

</LinearLayout>
"""
print (droid.fullShow(layoutMain))
EventMain()
droid.fullDismiss()
# -- END MAIN LAYOUT --


# //---------- E N D  L A Y O U T S ----------//
