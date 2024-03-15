import * as React from 'react';
import {useState, useEffect} from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { StyleSheet, Image, View, Text, TextInput, TouchableOpacity } from 'react-native';


export default function RegisterScreen({ navigation }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [validCredentials, setValidCredentials] = useState([]);
  
    useEffect(() => {
      const fetchValidCredentials = async () => {
        try {
          const validCredentialsJson = await AsyncStorage.getItem('validCredentials');
          if (validCredentialsJson) {
            setValidCredentials(JSON.parse(validCredentialsJson));
          } else {
          }
        } catch (error) {
        }
      };
  
      fetchValidCredentials();
    }, []);
  
    const handleRegister = async () => {
      if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
      }
  
      // Check if the username already exists
      if (validCredentials.some(cred => cred.username === username)) {
        alert('Username already exists');
        return;
      }
  
      // Save the new username and password
      const newValidCredentials = [...validCredentials, { username, password }];
      await AsyncStorage.setItem('validCredentials', JSON.stringify(newValidCredentials));
      console.log('Registered new user:', username);
  
      alert('Registration successful');
      // Navigate to 'Sign In' screen
      navigation.navigate('Sign In');
    };
  
    return(  
      <View style={styles.screenView}>
      
        <TextInput style={styles.URB} placeholder = 'Enter Username' value={username}
          onChangeText={text => setUsername(text)}/>
        <TextInput style={styles.PRB} placeholder = 'Enter Password' value={password}
          onChangeText={text => setPassword(text)}
          secureTextEntry/>
        <TextInput style={styles.P2RB} placeholder = 'Re-enter Password' value={confirmPassword}
          onChangeText={text => setConfirmPassword(text)}
          secureTextEntry/>
  
        <TouchableOpacity style={styles.registerButton} onPress={handleRegister}>
          <Text style={styles.buttonText}>Register</Text>
        </TouchableOpacity>
  
        <TouchableOpacity style={styles.g2sButton} onPress={() => navigation.navigate('Sign In')}>
          <Text style={styles.buttonText}>Back Out</Text>
        </TouchableOpacity>

        <Image style={styles.logoRegister} 
          resizeMode="contain" source={require('./Images/logo_ss.png')} />
        <Image style={styles.bnameRegister} 
          resizeMode="contain" source={require('./Images/bname_ss.png')} />
  
      </View>
    );
  }

  const styles = StyleSheet.create({
    screenView: {flex:1, backgroundColor: '#87cefa', alignItems:'center', justifyContent: 'center'},
    logoRegister: {bottom: 400, width: 250, height: 280},
  
    bnameRegister: {position: 'absolute', bottom:-50, width: 400, height: 280},
  
    registerButton: {alignItems: 'center', justifyContent: 'center',
      top: 260, width:180, height:65, backgroundColor: '#dcdcdc'},
    
    g2sButton: {alignItems: 'center', justifyContent: 'center',
      top: 290, width:180, height:65, backgroundColor: '#dcdcdc' , zIndex: 1},
    
    URB: {fontSize: 15, width:160, margin:12, borderWidth:2, padding: 10, top:200,
      justifyContent: 'center', backgroundColor: 'white'},
    
    PRB: {fontSize: 15, width:160, margin:12, borderWidth:2, padding: 10, top:220,
      justifyContent: 'center', backgroundColor: 'white'},
    
    P2RB: {fontSize: 15, width:160, margin:12, borderWidth:2, padding: 10, top:240,
      justifyContent: 'center', backgroundColor: 'white'},
  
    buttonText: {fontSize:20, fontWeight: 'bold'}
    }
    );