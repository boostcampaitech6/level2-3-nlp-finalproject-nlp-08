import React from "react";
import Box from "@mui/material/Box";
import "./FixedTextBox.css";

const FixedTextBox = ({ value, keywords, onButtonClick }) => {
  console.log("Keywords:", keywords);
  const regex = new RegExp(`(${keywords.join('|')})`, 'gi');
  const preParts = value.split(regex);
  const parts = preParts.map((prePart) => prePart.replace(/\. /g, ".\n\n"));

  console.log("Parts:", parts);

  return (
    <div className="result-container">
      <Box className="result-textbox">
        {parts.map((part, index) =>
          regex.test(part) ? (
            <button
              key={index}
              className="highlighted-button"
              variant="contained"
              onClick={() =>  {
                onButtonClick(part, parts[index]);
              }}
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
