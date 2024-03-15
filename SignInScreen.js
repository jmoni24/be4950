import * as React from 'react';
import {useState, useEffect} from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { StyleSheet, Image, View, Text, TextInput, TouchableOpacity } from 'react-native';


export default function SignInScreen({ navigation }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [validCredentials, setValidCredentials] = useState([]);
  
    useEffect(() => {
      const fetchValidCredentials = async () => {
        try {
          const validCredentialsJson = await AsyncStorage.getItem('validCredentials');
          if (validCredentialsJson) {
            const parsedCredentials = JSON.parse(validCredentialsJson);
            setValidCredentials(parsedCredentials);
            console.log('Fetched valid credentials:', parsedCredentials); // Add this console.log statement
          } else {
            console.log('No valid credentials found in storage.');
          }
        } catch (error) {
          console.error('Error fetching valid credentials:', error);
        }
      };
  
      fetchValidCredentials();
    }, []);
  
    const handleLogin = () => {
      // Check if the entered username and password match any valid combination
      const isValidCombo = validCredentials.some(cred => cred.username === username && cred.password === password);
  
      if (isValidCombo) {
        console.log('Login successful for user:', username);
        // Save username to AsyncStorage
        AsyncStorage.setItem('username', username);
        // Navigate to 'Data' screen
        navigation.navigate('Data');
      } else {
        alert('Invalid username or password');
      }
    };
  
    return(  
      <View style={styles.screenView}>
      
        <TextInput style={styles.USIB} placeholder = 'Username' value={username}
          onChangeText={text => setUsername(text)}/>
        <TextInput style={styles.PSIB} placeholder = 'Password' value={password}
          onChangeText={text => setPassword(text)} secureTextEntry/>
  
        <TouchableOpacity style={styles.loginButton} onPress={handleLogin} > 
          <Text style={styles.buttonText}> Login </Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.creataccountButton} onPress={() => navigation.navigate('Register')}>
          <Text style={styles.buttonText}> Create Account </Text>
        </TouchableOpacity>
        
        <Image style={styles.logoSignIn} 
          resizeMode="contain" source={require('./Images/logo_ss.png')} />
        <Image style={styles.bnameSignIn} 
          resizeMode="contain" source={require('./Images/bname_ss.png')} />

      </View>
    );
  }

  const styles = StyleSheet.create({
    // Screen Layout
    screenView: {flex:1, backgroundColor: '#87cefa', alignItems:'center', justifyContent: 'center'},
    // Sign In Screen
    logoSignIn: {bottom: 400, width: 250, height: 280},
    
    bnameSignIn: {position: 'absolute', bottom:-50, width: 400, height: 280},
    
    USIB: {fontSize: 15, width:160, margin:12, borderWidth:2, padding: 10, top:150,
            justifyContent: 'center', backgroundColor: 'white'},
    
    PSIB: {fontSize: 15, width:160, margin:12, borderWidth:2, padding: 10, top:170,
            justifyContent: 'center', backgroundColor: 'white'},
    loginButton: {alignItems: 'center', justifyContent: 'center', 
            top: 190, width:180, height:65, backgroundColor: '#dcdcdc'},
  
    creataccountButton: {alignItems: 'center', justifyContent: 'center', 
            top:220, width:180, height:65, backgroundColor: '#dcdcdc'},
  
    buttonText: {fontSize:20, fontWeight: 'bold'}
  });