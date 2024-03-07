import React from "react";
import Box from "@mui/material/Box";
import "./FixedTextBox.css";

const FixedTextBox = ({ value, answer }) => {
  const regex = new RegExp(`(${answer})`, "gi");
  const preParts = value.split(regex);
  const parts = preParts.map((prePart) => prePart.replace(/\. /g, ".\n\n"));

  console.log("Parts:", parts);
  const handleButtonClick = (clickedText) => {
    console.log(`Button clicked: ${clickedText}`);
  };

  return (
    <div className="result-container">
      <Box className="result-textbox">
        {parts.map((part, index) =>
          regex.test(part) ? (
            <button
              key={index}
              className="highlighted-button"
              variant="contained"
              onClick={() => handleButtonClick(part)}
            >
              {part}
            </button>
          ) : (
            <span key={index}>{part}</span>
          )
        )}
      </Box>
    </div>
  );
};

export default FixedTextBox;
