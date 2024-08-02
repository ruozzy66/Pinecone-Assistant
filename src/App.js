import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { ChakraProvider, Box, VStack, Input, Button, Text, Flex, Spacer } from '@chakra-ui/react';

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

    const newMessage = { role: 'user', content: input };
    setMessages([...messages, newMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chat', {
        messages: [...messages, newMessage],
      });

      const assistantMessage = response.data.chat_completion.choices[0].message;
      setMessages(prevMessages => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prevMessages => [...prevMessages, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChakraProvider>
      <Box maxWidth="600px" margin="auto" height="100vh" display="flex" flexDirection="column">
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
                <Text>{message.content}</Text>
              </Box>
            </Flex>
          ))}
          <div ref={messagesEndRef} />
        </VStack>
        <Flex padding={4}>
          <Input 
            value={input} 
            onChange={(e) => setInput(e.target.value)} 
            placeholder="Type a message..." 
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          />
          <Button 
            onClick={sendMessage} 
            marginLeft={2} 
            isLoading={isLoading}
            loadingText="Sending"
          >
            Send
          </Button>
        </Flex>
      </Box>
    </ChakraProvider>
  );
};

export default App;