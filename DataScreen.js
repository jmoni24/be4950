import * as React from 'react';
import {useState} from 'react';
import { StyleSheet, Image, View, Text} from 'react-native';
import DropDownPicker from 'react-native-dropdown-picker';

const pH_data = 5.4;
const temp_data = 99;
const imp_data = 100;

export default function DataScreen({ navigation }) {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState(null);
  const [items, setItems] = useState([
    {label: 'Sign Out', value: 'signin'},
    {label: 'Data', value: 'data'},
    {label: 'FAQ', value: 'faq'}
  ]);
  const handleItemSelect = (item) => {
  switch(item.value) {
    case 'signin':
      navigation.navigate('Sign In');
      break;
    case 'data':

      navigation.navigate('Data');
      break;
    case 'faq':
      navigation.navigate('FAQ');
      break;
    default:
      break;
    }
    setOpen(false); // Close the dropdown after selection
  };
  return(
    <View style={styles.screenView}>
      <Text style={styles.dataHeaders}>         pH{'\n'}{'\n'}{'\n'}
      Temperature{'\n'}{'\n'}{'\n'}Impedance</Text>
      <Text style={styles.datapH}>5.4{'\n'}{'\n'}{'\n'}{'\n'}</Text>
      <Text style={styles.dataTemp}>99&deg;F{'\n'}{'\n'}{'\n'}</Text>
      <Text style={styles.dataImp}>{'\n'}100Ω</Text>
      <DropDownPicker style={styles.dropdownMenuData} open={open} value={value} items={items} setOpen={setOpen} 
      setValue={setValue} setItems={setItems} placeholder = 'Menu' onSelectItem={handleItemSelect}
      dropDownContainerStyle={{ position: 'absolute', width: 100, top: -500, left: 300, zIndex: -10 }}/>
      <Image style={styles.logoData} 
        resizeMode="contain" source={require('./Images/logo_ss.png')} />
        <Image style={styles.bnameData} 
        resizeMode="contain" source={require('./Images/bname_ss.png')} />
    </View>
  );
}

const styles = StyleSheet.create({
  screenView: {flex:1, backgroundColor: '#87cefa', alignItems:'center', justifyContent: 'center'},
  dataHeaders: {fontSize: 45, top: 420, justifyContent: 'center', alignItems: 'center'},
  datapH: {fontSize: 35, top:150, justifyContent: 'center', alignItems: 'center', right: 10, color: 
      pH_data > 7.3 ? 'red' : 5.6 < pH_data && pH_data <= 7.3 ? 'yellow' : 'green'},
  dataTemp: {fontSize: 35, top:105, justifyContent: 'center', alignItems: 'center', right:10, color: 
      temp_data > 105.4 ? 'red' : 101.8 < temp_data && temp_data <= 105.4 ? 'yellow' : 'green'},
  dataImp: {fontSize: 35, top:60, justifyContent: 'center', alignItems: 'center', right:10, color: 
      imp_data < 80 ? 'red' : 80 < imp_data && imp_data <= 90 ? 'yellow' : 'green'},
  
  logoData: {bottom: 620, width: 150, height: 180},
  
  bnameData: {bottom: 160, width: 300, height: 220},
  
  signoutData: {alignItems: 'center', justifyContent: 'center', 
          top:120, width:180, height:65, backgroundColor: '#dcdcdc'},
  
  dropdownMenuData: {left: 300, top: -550, width: 100, backgroundColor: '#fafafa', borderColor: '#ccc', borderWidth: 1, 
          borderRadius: 5 },
  buttonText: {fontSize:20, fontWeight: 'bold'}
});