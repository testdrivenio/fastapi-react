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
  IconButton,
  useMultiStyleConfig,
} from "@chakra-ui/react";
import { CopyIcon, SunIcon } from "@chakra-ui/icons";

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

  const styles = useMultiStyleConfig("Button", { variant: "outline" });

  return (
    <Stack spacing={10} margin={10}>
      <Box>
        <Heading size="lg">Upload your resume</Heading>
      </Box>
      <Box alignItems={"center"} width={"50%"}>
        <form onSubmit={handleSubmit}>
          <InputGroup size="lg">
            <Input
              pr="9.5rem"
              type="file"
              placeholder="Upload a resume"
              aria-label="Upload a resume"
              onChange={handleInput}
              sx={{
                "::file-selector-button": {
                  border: "none",
                  outline: "none",
                  marginTop: 1,
                  marginBottom: 1,
                  mr: 2,
                  ...styles,
                },
              }}
            />
          </InputGroup>
        </form>
      </Box>
      <Box>
        <Button
          h="3.5rem"
          size="lg"
          onClick={handleSubmit}
          colorScheme={"teal"}
        >
          Upload
        </Button>
      </Box>

      <Box>
        <Heading size="lg">Past Jobs</Heading>
      </Box>

      {positions.map((position) => (
        <Position
          key={position["title"] + position["employerName"]}
          title={position["title"]}
          highlights={position["highlights"]}
          employerName={position["employerName"]}
          startDate={position["startDate"]}
          endDate={position["endDate"]}
        />
      ))}
    </Stack>
  );
}

function Position({ title, employerName, startDate, endDate, highlights }) {
  const [choices, setChoices] = useState([]);
  const [isGettingImprovements, setIsGettingImprovements] = useState(false);

  const handleSubmit = async () => {
    // run mutliple requests for each highlight
    setIsGettingImprovements(true);

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
      setIsGettingImprovements(false);
    });
  };

  return (
    <Box>
      <HStack marginBottom={5}>
        <Box>
          <Heading size="md">{title}</Heading>
          <Text size="md">
            {employerName}
            {", "}
            {startDate}
            {" to "} {endDate}
          </Text>
        </Box>
        <Button
          h="2.5rem"
          size="md"
          onClick={handleSubmit}
          colorScheme="whatsapp"
          style={{ marginLeft: 20 }}
          isLoading={isGettingImprovements}
          loadingText="Generating"
          spinnerPlacement="end"
        >
          Improve
        </Button>
      </HStack>

      {highlights.map((highlight, i) => (
        <Box key={highlight}>
          <Text fontSize="xl" marginBottom={5}>
            • {highlight}
          </Text>
          {choices.length > 0 &&
            choices[i] &&
            choices[i].map((choice) => (
              <HStack
                marginBottom={5}
                borderWidth="3px"
                padding={5}
                style={{ marginLeft: 20, borderRadius: 10 }}
              >
                <SunIcon color="yellow.500" w={5} h={5}></SunIcon>
                <Text fontSize="lg" marginBottom={5}>
                  {choice}
                </Text>
                <IconButton
                  colorScheme="blue"
                  aria-label="Copy"
                  icon={<CopyIcon />}
                  onClick={() => navigator.clipboard.writeText(choice)}
                />
              </HStack>
            ))}
        </Box>
      ))}
    </Box>
  );
}

export default function Resume() {
  return <UploadResume />;
}
