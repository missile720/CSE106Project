from re import S
import sqlite3
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.orm import backref, query

app = Flask(__name__)
conn = sqlite3.connect('genshindata.sqlite',check_same_thread=False)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///genshindata.sqlite"
app.config['SECRET_KEY'] = "thisissecret"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Login first!!!'
app.secret_key = 'keep it secret, keep it safe'

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable=False)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable=False)
    character = db.relationship('Tempcharacters', backref = 'player')
    artifact = db.relationship('Artifact', backref = 'player1')

    def check_password(self,password): #checks the password against the hash/salted in database
        return (sha256_crypt.verify(password,self.password)) 

    def __init__( self, username, password):
        self.username = username
        self.password = password

class Weapon(UserMixin, db.Model):
    weaponId = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable=False)
    weaponType = db.Column(db.String, nullable = False)
    weaponName = db.Column(db.String, nullable = False)
    weaponAttack = db.Column(db.Float, nullable = False)
    weaponSecondStat = db.Column(db.String, nullable = False)
    weaponSecondStatValue = db.Column(db.Float, nullable = False)
    tweapon = db.relationship('Tempcharacters', backref = 'reals')

class Artifact(UserMixin, db.Model):
    artifactId = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    artifactName = db.Column(db.String, nullable = False)
    artifactSlot = db.Column(db.String, nullable = False)
    artifactHPPercent = db.Column(db.Float, nullable = True)
    artifactHP = db.Column(db.Float, nullable = True)
    artifactAttackPercent = db.Column(db.Float, nullable = True)
    artifactAttack = db.Column(db.Float, nullable = True)
    artifactDefensePercent = db.Column(db.Float, nullable = True)
    artifactDefense = db.Column(db.Float, nullable = True)
    artifactElementalMastery = db.Column(db.Float, nullable = True)
    artifactCriticalRatePercent = db.Column(db.Float, nullable = True)
    artifactCriticalDamagePercent = db.Column(db.Float, nullable = True)
    artifactEnergyRecharge = db.Column(db.Float, nullable = True)
    artifactDamageBonus = db.Column(db.Float, nullable = True)

class Tempartifact(UserMixin, db.Model):
    artifactId = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable=False)
    artifactName = db.Column(db.String, nullable = False)
    artifactSlot = db.Column(db.String, nullable = False)
    artifactHPPercent = db.Column(db.Float, nullable = True)
    artifactHP = db.Column(db.Float, nullable = True)
    artifactAttackPercent = db.Column(db.Float, nullable = True)
    artifactAttack = db.Column(db.Float, nullable = True)
    artifactDefensePercent = db.Column(db.Float, nullable = True)
    artifactDefense = db.Column(db.Float, nullable = True)
    artifactElementalMastery = db.Column(db.Float, nullable = True)
    artifactCriticalRatePercent = db.Column(db.Float, nullable = True)
    artifactCriticalDamagePercent = db.Column(db.Float, nullable = True)
    artifactEnergyRecharge = db.Column(db.Float, nullable = True)
    artifactDamageBonus = db.Column(db.Float, nullable = True)

    def __init__( self, userId, artifactName,artifactSlot,artifactHPPercent,artifactHP,artifactAttackPercent,artifactAttack,artifactDefensePercent,
    artifactDefense,artifactElementalMastery,artifactCriticalRatePercent,artifactCriticalDamagePercent,artifactEnergyRecharge,artifactDamageBonus):
        self.userId = userId
        self.artifactName = artifactName
        self.artifactSlot = artifactSlot
        self.artifactHPPercent = artifactHPPercent
        self.artifactHP = artifactHP
        self.artifactAttackPercent = artifactAttackPercent
        self.artifactAttack = artifactAttack
        self.artifactDefensePercent = artifactDefensePercent
        self.artifactDefense = artifactDefense
        self.artifactElementalMastery = artifactElementalMastery
        self.artifactCriticalRatePercent = artifactCriticalRatePercent
        self.artifactCriticalDamagePercent = artifactCriticalDamagePercent
        self.artifactEnergyRecharge = artifactEnergyRecharge
        self.artifactDamageBonus = artifactDamageBonus

class Character(UserMixin, db.Model):
    characterId = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable=False)
    characterName = db.Column(db.String, nullable = False)
    characterHP = db.Column(db.Float, nullable = False)
    characterAttack = db.Column(db.Float, nullable = False)
    characterDefense = db.Column(db.Float, nullable = False)
    characterElementalMastery = db.Column(db.Float, nullable = False)
    characterCriticalRatePercent = db.Column(db.Float, nullable = False)
    characterCriticalDamagePercent = db.Column(db.Float, nullable = False)
    characterEnergyRecharge = db.Column(db.Float, nullable = False)
    characterSpecialStat = db.Column(db.String, nullable = True)
    characterSpecialStatValue = db.Column(db.Float, nullable = False)
    tcharacter = db.relationship('Tempcharacters', backref = 'real')

class Tempcharacters(UserMixin, db.Model):
    tempCharacterId = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable=False)
    characterId = db.Column(db.Integer, db.ForeignKey('character.characterId'), nullable=False)
    tempCharacterUserId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tempCharactername = db.Column(db.String, nullable = False)
    tempCharacterHP = db.Column(db.Float, nullable = False)
    tempCharacterAttack = db.Column(db.Float, nullable = False)
    tempCharacterDefense = db.Column(db.Float, nullable = False)
    tempCharacterElementalMastery = db.Column(db.Float, nullable = False)
    tempCharacterCriticalRatePercent = db.Column(db.Float, nullable = False)
    tempCharacterCriticalDamagePercent = db.Column(db.Float, nullable = False)
    tempCharactererEnergyRecharge = db.Column(db.Float, nullable = False)
    tempCharacterSpecialStat = db.Column(db.String, nullable = True)
    tempCharacterSpecialStatValue = db.Column(db.Float, nullable = False)
    tempCharacterWeaponId = db.Column(db.Integer, db.ForeignKey('weapon.weaponId'), nullable=True) 

    def __init__( self, tempCharacterUserId, tempCharactername,tempCharacterHP,tempCharacterAttack,tempCharacterDefense,
    tempCharacterElementalMastery,tempCharacterCriticalRatePercent,tempCharacterCriticalDamagePercent,tempCharactererEnergyRecharge,
    tempCharacterSpecialStat,tempCharacterSpecialStatValue,tempCharacterWeaponId,tempCharacterArtifact1,tempCharacterArtifact2,
    tempCharacterArtifact3,tempCharacterArtifact4,tempCharacterArtifact5):

        self.tempCharacterUserId = tempCharacterUserId
        self.tempCharactername = tempCharactername
        self.tempCharacterHP = tempCharacterHP
        self.tempCharacterAttack = tempCharacterAttack
        self.tempCharacterDefense = tempCharacterDefense
        self.tempCharacterElementalMastery = tempCharacterElementalMastery
        self.tempCharacterCriticalRatePercent = tempCharacterCriticalRatePercent
        self.tempCharacterCriticalDamagePercent = tempCharacterCriticalDamagePercent
        self.tempCharactererEnergyRecharge = tempCharactererEnergyRecharge
        self.tempCharacterSpecialStat = tempCharacterSpecialStat
        self.tempCharacterSpecialStatValue = tempCharacterSpecialStatValue
        self.tempCharacterWeaponId = tempCharacterWeaponId
        self.tempCharacterArtifact1 = tempCharacterArtifact1
        self.tempCharacterArtifact2 = tempCharacterArtifact2
        self.tempCharacterArtifact3 = tempCharacterArtifact3
        self.tempCharacterArtifact4 = tempCharacterArtifact4
        self.tempCharacterArtifact5 = tempCharacterArtifact5


class Team(UserMixin, db.Model):
    teamId = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teamMember1 = db.Column(db.Integer, db.ForeignKey('tempcharacters.tempCharacterId'),nullable = False)
    teamMember2 = db.Column(db.Integer, db.ForeignKey('tempcharacters.tempCharacterId'),nullable = False)
    teamMember3 = db.Column(db.Integer, db.ForeignKey('tempcharacters.tempCharacterId'),nullable = False)
    teamMember4 = db.Column(db.Integer, db.ForeignKey('tempcharacters.tempCharacterId'),nullable = False)
    shared = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    def __init__( self, userId, teamMember1, teamMember2, teamMember3, teamMember4, shared, likes):
        self.userId = userId
        self.teamMember1 = teamMember1
        self.teamMember2 = teamMember2
        self.teamMember3 = teamMember3
        self.teamMember4 = teamMember4
        self.shared = shared
        self.likes = likes

class Comment(UserMixin, db.Model):
    commentId = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable=False)
    commentTeamId = db.Column(db.Integer, db.ForeignKey('team.teamId'), nullable=False)
    comment = db.Column(db.String, nullable = True)
    
    def __init__( self, commentId, commentTeamId, comment):
        self.commentId = commentId
        self.commentTeamId = commentTeamId
        self.comment = comment

class Artifactset(UserMixin, db.Model):
    artifactSetId = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable=False)
    artifactSetName = db.Column(db.String, nullable = False)
    artifactSetComment = db.Column(db.String, nullable = False)  

db.create_all()

@app.route('/', methods = ['GET'])
def home():
    return render_template('firstPage.html')

@app.route('/login', methods = ['GET'])
def login():
    return render_template('loginPage.html')

@app.route('/signup', methods = ['GET'])
def signup():
    return render_template('signUpPage.html')

@app.route('/register', methods = ['POST'])
def register():
    usernam = request.form['Email']
    password = request.form['Password']
    user = User.query.filter_by(username = usernam).first() 

    if user is not None:
        return redirect(url_for('login'))

    #hash/salt password
    encryptPassword = sha256_crypt.encrypt(password)

    newUser = User(usernam,encryptPassword)
    db.session.add(newUser)
    db.session.commit()

    return render_template('firstPage.html')

@app.route('/logmein', methods = ['POST'])
def logmein():
    user = User.query.filter_by(username=request.form['Email']).first() 
    if user is None or not user.check_password(request.form['Password']):
        return redirect(url_for('login'))

    login_user(user)

    return redirect(url_for('user'))

@app.route('/user')
@login_required
def user():
   return render_template('userPage.html')

@app.route('/playerteams')
@login_required
def playerteams():
    
   query = """SELECT username, character1.characterName, character2.characterName, character3.characterName, character4.characterName
          FROM user, Character character1, Character character2, Character character3, Character character4, team
          where userId = id
          and teamMember1 = character1.characterId
          and teamMember2 = character2.characterId
          and teamMember3 = character3.characterId
          and teamMember4 = character4.characterId
          and shared = 1
          ;"""

   cursor = conn.cursor()
   cursor.execute(query)
   lists = cursor.fetchall()
   return render_template('teamListPage.html',results = lists)

@app.route('/teammanage')
@login_required
def teampage():
    currentUser = User.query.filter_by(id=current_user.id).first()

    uid = currentUser.id
        
    query = f"""SELECT character1.characterName, character2.characterName, character3.characterName, character4.characterName
          FROM Character character1, Character character2, Character character3, Character character4, team
          where userId = "{uid}"
          and teamMember1 = character1.characterId
          and teamMember2 = character2.characterId
          and teamMember3 = character3.characterId
          and teamMember4 = character4.characterId
          ;"""

    cursor = conn.cursor()
    cursor.execute(query)
    lists = cursor.fetchall()
    return render_template('addTeamPage.html',results = lists)

@app.route('/characterstatcalc', methods = ['GET'])
@login_required
def charcatercalc():

    query = """SELECT characterName
            FROM character
            ;"""
    query2 = """SELECT weaponName
            FROM weapon
            ;"""
    query3 = """SELECT artifactId, artifactName
            FROM artifact
            where artifactSlot = 'flower'
            ;"""
    query4 = """SELECT artifactId, artifactName
            FROM artifact
            where artifactSlot = 'plume'
            ;"""
    query5 = """SELECT artifactId, artifactName
            FROM artifact
            where artifactSlot = 'sand'
            ;"""
    query6 = """SELECT artifactId, artifactName
            FROM artifact
            where artifactSlot = 'goblet'
            ;"""
    query7 = """SELECT artifactId, artifactName
            FROM artifact
            where artifactSlot = 'circlet'
            ;"""
    query8 = """SELECT artifactId, artifactName,artifactSlot, artifactHPPercent, artifactHP, artifactAttackPercent, artifactAttack, artifactDefensePercent, artifactDefense, artifactElementalMastery, artifactCriticalRatePercent, artifactCriticalDamagePercent, artifactEnergyRecharge, artifactDamageBonus
            FROM artifact
            ;"""
    cursor = conn.cursor()
    cursor.execute(query)
    list1 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query2)
    list2 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query3)
    list3 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query4)
    list4 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query5)
    list5 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query6)
    list6 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query7)
    list7 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query8)
    list8 = cursor.fetchall()

    # ch = request.form['Email']
    return render_template('CStatCalc.html', list1 = list1,list2 = list2,list3 = list3,list4 = list4,list5 = list5,list6 = list6,list7= list7,list8=list8)

@app.route('/finalstat', methods = ['POST'])
@login_required
def showfinal():
    c = request.form['character']
    w = request.form['weapon']
    f = request.form['flower']
    p = request.form['plume']
    s = request.form['sand']
    g = request.form['goblet']
    c2 = request.form['circlet']

    # get selected artifact from user 
    selected1=f
    selected2=p
    selected3=s
    selected4=g
    selected5=c2
    #get c_id from character user choose 
    chara = c
    #get w_id from weapon user choose 
    weap = w
    # empty temp
    cursor = conn.cursor()
    cmd="""Delete from tempartifact;"""
    cursor.execute(cmd)
    cursor = conn.cursor()
    # insert selected artifact to temptable 
    cmd0 = f"""
    INSERT INTO tempartifact(artifactId,artifactName,artifactSlot,artifactHPPercent,artifactHP,artifactAttackPercent,artifactAttack,artifactDefensePercent,artifactDefense,artifactElementalMastery,artifactCriticalRatePercent,artifactCriticalDamagePercent,artifactEnergyRecharge,artifactDamageBonus)
    select artifactId,artifactName,artifactSlot,artifactHPPercent,artifactHP,artifactAttackPercent,artifactAttack,artifactDefensePercent,artifactDefense,artifactElementalMastery,artifactCriticalRatePercent,artifactCriticalDamagePercent,artifactEnergyRecharge,artifactDamageBonus
    from artifact
    where artifactId = {selected1} or artifactId = {selected2} or artifactId = {selected3} or artifactId = {selected4} or artifactId = {selected5} ;
    """
    cursor.execute(cmd0)
    cursor = conn.cursor()
    # calculate the artifact 
    cmd1 = """
    select sum(artifactHPPercent),sum(artifactHP),sum(artifactAttackPercent),sum(artifactAttack),sum(artifactDefensePercent),sum(artifactDefense),sum(artifactElementalMastery),sum(artifactCriticalRatePercent),sum(artifactCriticalDamagePercent),sum(artifactEnergyRecharge)
    from tempartifact;
    """ 
    cursor.execute(cmd1)
    resultsA = cursor.fetchall()
    cursor = conn.cursor()
    # get chara 
    cmd2 = f"""
    select * from character
    where characterName = "{chara}";
    """
    cursor.execute(cmd2)
    resultsC = cursor.fetchall()
    cursor = conn.cursor()
    # get Weapon
    cmd3 = f"""
    select * from weapon
    where weaponName = "{weap}";
    """
    cursor.execute(cmd3)
    resultsW = cursor.fetchall()
    
    # get damagebonus from artifact 
    cmd4 = f"""
    select artifactDamageBonus from tempartifact
    where artifactDamageBonus != 'NULL';
    """
    cursor.execute(cmd4)
    resultsADB = cursor.fetchall()
    for resultADB in resultsADB:
        adb = resultADB[0]

    for resultW in resultsW:
        wpatk = resultW[3]
        wpsecond = resultW[4]
        wpvalue = resultW[5]

    for resultA in resultsA:
        hpp = resultA[0]
        hp = resultA[1]
        atkp = resultA[2]
        atk = resultA[3]
        defp = resultA[4]
        deff = resultA[5]
        em = resultA[6]
        cr = resultA[7]
        cd = resultA[8]
        er = resultA[9]
    
    # if none set to 0 
    if hpp is None:
        hpp = 0
    if hpp is None:
        hp = 0
    if atkp is None:
        atkp = 0
    if atk is None:
        atk = 0
    if defp is None:
        defp = 0
    if deff is None:
        deff = 0
    if em is None:
        em = 0
    if cr is None:
        cr = 0
    if cd is None:
        cd = 0
    if er is None:
        er = 0
    

    for resultC in resultsC:
        chp = resultC[2]
        catk = resultC[3]
        cdef = resultC[4]
        cem = resultC[5]
        ccr = resultC[6]
        ccd = resultC[7]
        cer = resultC[8]
        cdb = resultC[9]
        csv = resultC[10]
   
    shp = 0
    shpp = 0
    ahp = 0
    satk = 0
    satkp = 0
    aatk = 0
    sdef = 0
    sdefp = 0
    adef = 0
    sem = 0
    scr = 0
    scd = 0
    ser = 0
    Pyro = 0
    Hydro = 0
    Anemo = 0
    Electro = 0
    Cryo = 0
    Geo = 0
    Physical = 0

    # put value from chara to sum of each stats 
    if cdb is not None:
        if cdb == 'atk':
            satkp = satkp+csv
        if cdb == 'hp':
            shpp = shpp+csv
        if cdb == 'def':
            sdefp = sdefp+csv
        if cdb == 'Pyro':
            Pyro = Pyro+csv
        if cdb == 'Hydro':
            Hydro = Hydro+csv
        if cdb == 'Anemo':
            Anemo = Anemo+csv
        if cdb == 'Electro':
            Electro = Electro+csv
        if cdb == 'Cryo':
            Cryo = Cryo+csv
        if cdb == 'Geo':
            Geo =Geo+csv
        if cdb == 'Physical':
            Physical = Physical+csv
    shp = shp + chp
    satk = satk + catk
    sdef = sdef + cdef
    sem = sem + cem
    scr = scr + ccr
    scd = scd + ccd
    ser = ser + cer

    #time for weapon to sum 
    if wpsecond is not 'None':
        if wpsecond == 'atk':
            satkp = satkp+wpvalue
        if wpsecond == 'hp':
            shpp = shpp+wpvalue
        if wpsecond == 'def':
            sdefp = sdefp+wpvalue
        if wpsecond == 'cr':
            scr = scr + wpvalue
        if wpsecond == 'cd':
            scd = scd + wpvalue
        if wpsecond == 'er':
            ser = ser + wpvalue
        if wpsecond == 'em':
            sem = sem + wpvalue
        if wpsecond == 'Physical':
            Physical = Physical+wpvalue
    satk = satk + wpatk

    #last artifact
    shpp = shpp + hpp
    ahp = ahp + hp
    satkp = satkp + atkp
    aatk = aatk + atk
    sdefp = sdefp + defp
    adef = adef + deff
    sem = sem + em
    scr = scr + cr
    scd = scd + cd
    ser = ser + er
    if adb == 'pyro':
        Pyro = Pyro+46.6
    if adb == 'hydro':
        Hydro = Hydro+46.6
    if adb == 'anemo':
        Anemo = Anemo+46.6
    if adb == 'electro':
        Electro = Electro+46.6
    if adb == 'cryo':
        Cryo = Cryo+46.6
    if adb == 'geo':
        Geo =Geo+46.6
    if adb == 'physical':
        Physical = Physical+58.3

    #put all % to 1 if its 0 
    if shpp == 0:
        shpp = 1
    if satkp == 0:
        satkp = 1
    if sdefp == 0:
        sdefp = 1

    #finally end 
    fhp = shp + shp*shpp/100 + ahp
    fatk = satk + satk*satkp/100 + aatk
    fdef = sdef + sdef*sdefp/100 + adef
    return render_template('finalstat.html',c = c,w = w, hp = fhp,atk = fatk,deff=fdef,em = sem,cr = scr,cd = scd,er=ser,Pyro = Pyro,Hydro=Hydro,Anemo=Anemo,Electro=Electro,Cryo=Cryo,Geo=Geo,Physical=Physical)

@app.route('/addTeam/')
@login_required
def addTeam():
    query = """SELECT characterName
            FROM character
            ;"""
    cursor = conn.cursor()
    cursor.execute(query)
    list1 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query)
    list2 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query)
    list3 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query)
    list4 = cursor.fetchall()

    return render_template('addTeam.html', list1 = list1, list2 = list2, list3 = list3,list4 = list4)

@app.route('/removeteam')
@login_required
def removeteam():
    currentUser = User.query.filter_by(id=current_user.id).first()

    uid = currentUser.id
        
    query = f"""SELECT teamId,character1.characterName, character2.characterName, character3.characterName, character4.characterName
          FROM Character character1, Character character2, Character character3, Character character4, team
          where userId = "{uid}"
          and teamMember1 = character1.characterId
          and teamMember2 = character2.characterId
          and teamMember3 = character3.characterId
          and teamMember4 = character4.characterId
          ;"""
    cursor = conn.cursor()
    cursor.execute(query)
    list = cursor.fetchall()

    return render_template('deleteTeam.html', list1 = list)

@app.route('/add', methods = ['POST'])
@login_required
def add():
    c1 = request.form['character1']
    c2 = request.form['character2']
    c3 = request.form['character3']
    c4 = request.form['character4']
    
    query1 = f"""SELECT characterId
            FROM character
            where characterName = "{c1}"
            ;"""

    query2 = f"""SELECT characterId
            FROM character
            where characterName = "{c2}"
            ;"""
    query3 = f"""SELECT characterId
            FROM character
            where characterName = "{c3}"
            ;"""
    query4 = f"""SELECT characterId
            FROM character
            where characterName = "{c4}"
            ;"""

    cursor = conn.cursor()
    cursor.execute(query1)
    list1 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query2)
    list2 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query3)
    list3 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query4)
    list4 = cursor.fetchall()

    for row in list1:
        chara1 = row[0]

    for row in list2:
        chara2 = row[0]

    for row in list3:
        chara3 = row[0]

    for row in list4:
        chara4 = row[0]

    currentUser = User.query.filter_by(id=current_user.id).first()

    uid = currentUser.id

    newTeam = Team(uid,chara1,chara2,chara3,chara4,0,0)
    db.session.add(newTeam)
    db.session.commit()   

    #load players team 
    currentUser = User.query.filter_by(id=current_user.id).first()
    uid = currentUser.id
   
    query = f"""SELECT character1.characterName, character2.characterName, character3.characterName, character4.characterName
          FROM Character character1, Character character2, Character character3, Character character4, team
          where userId = "{uid}"
          and teamMember1 = character1.characterId
          and teamMember2 = character2.characterId
          and teamMember3 = character3.characterId
          and teamMember4 = character4.characterId
          ;"""

    cursor = conn.cursor()
    cursor.execute(query)
    lists = cursor.fetchall()

    return render_template('addTeamPage.html', results = lists)

@app.route('/delete', methods = ['POST'])
@login_required
def delete():
    t1 = request.form['team']

    team = Team.query.filter_by(teamId=t1).first()
    db.session.delete(team)
    db.session.commit()

    #load players team 
    currentUser = User.query.filter_by(id=current_user.id).first()
    uid = currentUser.id

    query = f"""SELECT character1.characterName, character2.characterName, character3.characterName, character4.characterName
          FROM Character character1, Character character2, Character character3, Character character4, team
          where userId = "{uid}"
          and teamMember1 = character1.characterId
          and teamMember2 = character2.characterId
          and teamMember3 = character3.characterId
          and teamMember4 = character4.characterId
          ;"""

    cursor = conn.cursor()
    cursor.execute(query)
    lists = cursor.fetchall()
    return render_template('addTeamPage.html', results = lists)

@app.route('/share', methods = ['POST'])
@login_required
def share():
    t1 = request.form['team']

    team = Team.query.filter_by(teamId=t1).first()
    if team.shared == 0:
        team.shared = 1
    elif team.shared == 1:
        team.shared = 0
    db.session.commit()

    #load players team 
    currentUser = User.query.filter_by(id=current_user.id).first()
    uid = currentUser.id

    query = f"""SELECT character1.characterName, character2.characterName, character3.characterName, character4.characterName
          FROM Character character1, Character character2, Character character3, Character character4, team
          where userId = "{uid}"
          and teamMember1 = character1.characterId
          and teamMember2 = character2.characterId
          and teamMember3 = character3.characterId
          and teamMember4 = character4.characterId
          ;"""

    cursor = conn.cursor()
    cursor.execute(query)
    lists = cursor.fetchall()
    return render_template('addTeamPage.html', results = lists)

@app.route('/shareteam')
@login_required
def shareteam():
    currentUser = User.query.filter_by(id=current_user.id).first()

    uid = currentUser.id
        
    query = f"""SELECT teamId,character1.characterName, character2.characterName, character3.characterName, character4.characterName, shared
          FROM Character character1, Character character2, Character character3, Character character4, team
          where userId = "{uid}"
          and teamMember1 = character1.characterId
          and teamMember2 = character2.characterId
          and teamMember3 = character3.characterId
          and teamMember4 = character4.characterId
          ;"""
    cursor = conn.cursor()
    cursor.execute(query)
    list = cursor.fetchall()

    return render_template('shareTeam.html', list1 = list)

@app.route('/editteam')
@login_required
def editteam():
    currentUser = User.query.filter_by(id=current_user.id).first()

    uid = currentUser.id
        
    query = f"""SELECT teamId,character1.characterName, character2.characterName, character3.characterName, character4.characterName, shared
          FROM Character character1, Character character2, Character character3, Character character4, team
          where userId = "{uid}"
          and teamMember1 = character1.characterId
          and teamMember2 = character2.characterId
          and teamMember3 = character3.characterId
          and teamMember4 = character4.characterId
          ;"""
    cursor = conn.cursor()
    cursor.execute(query)
    list = cursor.fetchall()

    query = """SELECT characterName
            FROM character
            ;"""
    cursor = conn.cursor()
    cursor.execute(query)
    list1 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query)
    list2 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query)
    list3 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query)
    list4 = cursor.fetchall()
    return render_template('editTeam.html', list1 = list, list2 = list1, list3 = list2, list4 = list3, list5 = list4)

@app.route('/edit', methods = ['POST'])
@login_required
def edit():
    t1 = request.form['team']    
    c1 = request.form['character1']
    c2 = request.form['character2']
    c3 = request.form['character3']
    c4 = request.form['character4']
    
    query1 = f"""SELECT characterId
            FROM character
            where characterName = "{c1}"
            ;"""

    query2 = f"""SELECT characterId
            FROM character
            where characterName = "{c2}"
            ;"""
    query3 = f"""SELECT characterId
            FROM character
            where characterName = "{c3}"
            ;"""
    query4 = f"""SELECT characterId
            FROM character
            where characterName = "{c4}"
            ;"""

    cursor = conn.cursor()
    cursor.execute(query1)
    list1 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query2)
    list2 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query3)
    list3 = cursor.fetchall()
    cursor = conn.cursor()
    cursor.execute(query4)
    list4 = cursor.fetchall()

    for row in list1:
        chara1 = row[0]

    for row in list2:
        chara2 = row[0]

    for row in list3:
        chara3 = row[0]

    for row in list4:
        chara4 = row[0]

    currentUser = User.query.filter_by(id=current_user.id).first()

    uid = currentUser.id
    editTeam = Team.query.filter_by(teamId=t1).first()
    editTeam.teamMember1 = chara1
    editTeam.teamMember2 = chara2
    editTeam.teamMember3 = chara3
    editTeam.teamMember4 = chara4
    db.session.commit()   

    #load players team 
    currentUser = User.query.filter_by(id=current_user.id).first()
    uid = currentUser.id
   
    query = f"""SELECT character1.characterName, character2.characterName, character3.characterName, character4.characterName
          FROM Character character1, Character character2, Character character3, Character character4, team
          where userId = "{uid}"
          and teamMember1 = character1.characterId
          and teamMember2 = character2.characterId
          and teamMember3 = character3.characterId
          and teamMember4 = character4.characterId
          ;"""

    cursor = conn.cursor()
    cursor.execute(query)
    lists = cursor.fetchall()

    return render_template('addTeamPage.html', results = lists)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return render_template('firstPage.html')

if __name__ == '__main__':
    app.run(debug = True)