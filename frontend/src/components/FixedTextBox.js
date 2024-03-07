import React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import './FixedTextBox.css';

const FixedTextBox = ({ value, answer }) => {
  const regex = new RegExp(`(${answer})`, 'gi');
  const parts = value.split(regex);

  const handleButtonClick = (clickedText) => {
    // 클릭된 텍스트에 대한 동작을 정의하세요.
    console.log(`Button clicked: ${clickedText}`);
    // 예를 들어, 클릭된 텍스트를 상태로 관리하거나 특정 함수를 호출할 수 있습니다.
  };

  return (
    <div className="result-container">
      <Box className="result-textbox">
        {parts.map((part, index) => (
          regex.test(part) ? (
            <Button key={index} className="highlighted-button" variant="contained" onClick={() => handleButtonClick(part)}>
              {part}
            </Button>
          ) : (
            <span key={index}>{part}</span>
          )
        ))}
      </Box>
      
    </div>
  );
};

export default FixedTextBox;
