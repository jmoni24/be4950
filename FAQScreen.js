import * as React from 'react';
import {useState} from 'react';
import {StyleSheet, Text, View } from 'react-native';
import DropDownPicker from 'react-native-dropdown-picker';

export default function FAQScreen ({navigation}){
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
      <Text style={styles.infoHeaders}>What is pH?{'\n'}{'\n'}{'\n'}{'\n'}{'\n'}{'\n'}
        What does temperature mean for my injury?{'\n'}{'\n'}{'\n'}{'\n'}{'\n'}
        What is impedance?
      </Text>
      <Text style={styles.infoText}>     pH is a way to measure how acidic or basic a substance is. It's a scale from 0 to 14, where
        lower numbers mean something is more acidic, higher numbers mean its more basic, and 7 is
        neutral. The pH of a healthy person's skin is between 4.2 and 5.6. However after an infection,
        the pH of the skin will rise above 7.3. {'\n'}{'\n'}{'\n'}{'\n'}{'\n'}
      </Text>
      <Text style={styles.infoText}>     When it comes to checking for an infection if the area around the injury feels warmer
        than usual, it might mean there's inflammation and a possible infection. An increase of 1.8&deg;F
        to 5.4&deg;F from your normal skin temperature can be a cause for concern. {'\n'}{'\n'}{'\n'}
      </Text>
      <Text style={styles.infoText}>     Skin impedance is the skin's resistance to electrical flow. Changes in skin impedance
        may potentially signal an infection due to inflammation, edema, or the presence of bacteria. 
        If your impedance is lower than normal, it may be cause for concern.
      </Text>
      <DropDownPicker style={styles.dropdownMenuFAQ} open={open} value={value} items={items} setOpen={setOpen} 
      setValue={setValue} setItems={setItems} placeholder = 'Menu' onSelectItem={handleItemSelect}
      dropDownContainerStyle={{ position: 'absolute', width: 100, top: -850, left: 300, zIndex: -10 }}/>
    </View>
  );
}

  const styles = StyleSheet.create({
    screenView: {flex:1, backgroundColor: '#87cefa', alignItems:'center', justifyContent: 'center'},
    dropdownMenuFAQ: {left: 300, top: -900, width: 100, backgroundColor: '#fafafa', borderColor: '#ccc', borderWidth: 1, 
          borderRadius: 5 },
    infoHeaders: {fontSize: 35, top: 280, justifyContent: 'center', alignItems: 'center', textAlign: 'center'},
    infoText: {fontSize: 20, top: -180, justifyContent: 'center', alignItems: 'center'}
  });