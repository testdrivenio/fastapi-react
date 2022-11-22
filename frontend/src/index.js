import React from "react";
import { render } from 'react-dom';
// import { ChakraProvider } from "@chakra-ui/core";
import { ChakraProvider } from '@chakra-ui/react';

import Header from "./Components/Header";
import Todos from "./Components/Todos";

function App() {
  return (
    <ChakraProvider>
      <Header />
      <Todos />
    </ChakraProvider>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)
