import React, { useState } from 'react';
import NormalButton from './NormalButton'; // Adjust the import path accordingly

function InputTextBox() {
  const [textBoxValue, setTextBoxValue] = useState('');

  const handleDeleteAllClick = () => {
    // Clear the text box by setting its value to an empty string
    setTextBoxValue('');
  };

  return (
    <div>
      <textarea
        value={textBoxValue}
        onChange={(e) => setTextBoxValue(e.target.value)}
      />

      <NormalButton label="Delete All" onClick={handleDeleteAllClick} />
    </div>
  );
}

export default InputTextBox;