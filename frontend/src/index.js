import React from "react";
import { render } from 'react-dom';
// import { ChakraProvider } from "@chakra-ui/core";
import { ChakraProvider } from '@chakra-ui/react';
import { Spacer } from "@chakra-ui/react";


import Header from "./Components/Header";
import Resume from "./Components/Resume";

function App() {
  return (
    <ChakraProvider>
      <Header />
      <Spacer />
      <Resume />
    </ChakraProvider>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)
