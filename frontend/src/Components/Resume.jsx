import React, { useState } from "react";
import {
  Button,
  Input,
  InputGroup,
  Stack,
  Heading,
  Box,
  Text,
  HStack,
} from "@chakra-ui/react";

function UploadResume() {
  const [resume, setResume] = useState(null);
  const [positions, setPositions] = useState([]);
  // const {positions, fetchPositions} = React.useContext(PositionsContext)

  const handleInput = (event) => {
    setResume(event.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("resume", resume);

    const response = await fetch("http://localhost:8000/resume/highlights", {
      method: "POST",
      body: formData,
    });
    const positionsJson = await response.json();
    setPositions(positionsJson["data"]);
  };

  return (
    <Stack spacing={10} margin={10}>
      <Box>
        <Heading size="lg">Upload your resume</Heading>
      </Box>
      <Box alignItems={"center"} width={"50%"}>
        <form onSubmit={handleSubmit}>
          <InputGroup size="lg">
            <Input
              pr="4.5rem"
              type="file"
              placeholder="Upload a resume"
              aria-label="Upload a resume"
              onChange={handleInput}
            />
          </InputGroup>
        </form>
      </Box>
      <Box>
        <Button h="3.5rem" size="lg" onClick={handleSubmit}>
          Upload
        </Button>
      </Box>

      <Box>
        <Heading size="lg">Past Jobs</Heading>
      </Box>

      {positions.map((position) => (
        <Position
          title={position["title"]}
          highlights={position["highlights"]}
        />
      ))}
    </Stack>
  );
}

function Position({ title, highlights }) {
  const [choices, setChoices] = useState([]);

  const handleSubmit = async () => {
    // run mutliple requests for each highlight

    const choices = highlights.map(async (highlight) => {
      const url = `http://localhost:8000/resume/improvement`;
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ highlight: highlight }),
      });
      const improvementsJson = await response.json();
      return improvementsJson["data"];
    });

    Promise.all(choices).then((values) => {
      setChoices(values);
    });
  };

  return (
    <Box>
      <HStack>
        <Heading size="md" marginBottom={5}>
          {title}
        </Heading>
        <Button h="2.5rem" size="md" onClick={handleSubmit}>
          Improve
        </Button>
      </HStack>

      {highlights.map((highlight, i) => (
        <Box>
          <Text fontSize="lg" marginBottom={5}>
            {highlight}
          </Text>
          {choices.length > 0 &&
            choices[i] &&
            choices[i].map((choice) => (
              <Text fontSize="md" marginBottom={5} style={{ textIndent: 20 }}>
                {choice}
              </Text>
            ))}
        </Box>
      ))}
    </Box>
  );
}

export default function Resume() {
  return <UploadResume />;
}
