import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { ChakraProvider, Box, VStack, Input, Button, Text, Flex, Spinner, CSSReset } from '@chakra-ui/react';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (input.trim() === '') return;

    console.log('Sending message:', input);
    const newMessage = { role: 'user', content: input };
    setMessages(prevMessages => [...prevMessages, newMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chat', {
        messages: [...messages, newMessage],
      });
      console.log('Server response:', response.data);
      
      if (response.data && response.data.choices && response.data.choices.length > 0) {
        const assistantMessage = response.data.choices[0].message;
        setMessages(prevMessages => [...prevMessages, assistantMessage]);
      } else {
        console.error('Unexpected response structure:', response.data);
        throw new Error('Unexpected response structure');
      }
    } catch (error) {
      console.error('Error in chat request:', error);
      setMessages(prevMessages => [...prevMessages, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChakraProvider>
      <CSSReset />
      <style>{`
        html, body {
          margin: 0;
          padding: 0;
          width: 100%;
          height: 100%;
        }
      `}</style>
      <Box maxWidth="600px" margin="auto" height="100vh" display="flex" flexDirection="column">
        <Text fontSize="xl" textAlign="center" position="fixed" top="0" left="50%" transform="translateX(-50%)" width="100%" backgroundColor="white" zIndex="1000">
          Twilight Imperium Fourth Edition Rules AI Assistant
        </Text>
        <Box mt="50px" flex={1} display="flex" flexDirection="column">
          <VStack 
            spacing={4} 
            align="stretch" 
            flex={1} 
            overflowY="auto" 
            padding={4}
            css={{
              '&::-webkit-scrollbar': {
                width: '4px',
              },
              '&::-webkit-scrollbar-track': {
                width: '6px',
              },
              '&::-webkit-scrollbar-thumb': {
                background: 'gray.300',
                borderRadius: '24px',
              },
            }}
          >
            {messages.map((message, index) => (
              <Flex key={index} justifyContent={message.role === 'user' ? 'flex-end' : 'flex-start'}>
                <Box 
                  maxWidth="70%" 
                  backgroundColor={message.role === 'user' ? 'blue.500' : 'gray.200'}
                  color={message.role === 'user' ? 'white' : 'black'}
                  borderRadius="lg" 
                  padding={3}
                >
                  <div dangerouslySetInnerHTML={{ __html: message.content }} />
                </Box>
              </Flex>
            ))}
            {isLoading && (
              <Flex justifyContent="flex-start">
                <Spinner size="sm" />
              </Flex>
            )}
            <div ref={messagesEndRef} />
          </VStack>
          <Flex padding={4}>
            <Input 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              placeholder="Type a message..." 
              onKeyDown={(e) => e.key === 'Enter' && !isLoading && sendMessage()}
              disabled={isLoading}
            />
            <Button 
              onClick={sendMessage} 
              marginLeft={2} 
              isLoading={isLoading}
              loadingText="Sending"
              disabled={isLoading || input.trim() === ''}
            >
              Send
            </Button>
          </Flex>
        </Box>
      </Box>
    </ChakraProvider>
  );
};

export default App;
