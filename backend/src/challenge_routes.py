""" 
    This module is responsible for managing the creation, deletion, edition and user login.
"""

from flask import Flask, jsonify, make_response, request
from src.mariaDB.query_users import user_exists, get_user_password
from src.utils.HashManager import HashManager
from src.utils.CipherManager import CipherManager
from flask import Blueprint
import logging
logging.basicConfig(level=logging.DEBUG)

challenges_bp = Blueprint('challenges', __name__)

@challenges_bp.route('/create_challenge', methods=['POST'])
def create_challenge():
    """Creates a new challenge in the database
    Return: returns a response object
    """
    data = request.get_json()
    title = data.get('title')
    document = data.get('document')
    userToShare = data.get('userToShare')
    userLogged = data.get('userLogged')
    
    if  len(userLogged) == 0:
            response = make_response(jsonify({"response": "There is no user logged"}), 422)
            return response
    
    hashedUser = HashManager.create_hash(userLogged)
    if len(userToShare) == 0: # if challenge is public, cypher it with admin password hash
          adminHash = HashManager.create_hash('admin') # unsafe as fuck, but what we can do...
          logging.debug("%s", adminHash)
          titleHash = HashManager.create_hash(title)
          documentHash = HashManager.create_hash(document)
          cipheredTitle = CipherManager.cipherChallengeAES(adminHash, titleHash)
          cipheredMessage = CipherManager.cipherChallengeAES(adminHash, documentHash)

          response = make_response(jsonify({"response": {"title": cipheredTitle, "message": cipheredMessage, "userShared": userToShare, "userLogged": hashedUser}}))
          return response 

    else:
          pass
          
    #TODO: create AES method
    #cipheredDocument = cipherAES(document)
    #cipheredTitle = cipherAES(title)
    
    #TODO: insert challenge into database
    #if insert_challenge(cipheredTitle, cipheredDocument, hashedUser, hashedToShareUser):
    #        response = make_response(jsonify({"response": "Challenge inserted"}), 401)
    #        return response 

    
