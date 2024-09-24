"use client"

import React, { useState } from 'react'
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const Button = ({ onClick, disabled, children }) => (
  <button
    className={`px-4 py-2 rounded ${disabled
        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
        : 'bg-blue-500 text-white hover:bg-blue-600'
      }`}
    onClick={onClick}
    disabled={disabled}
  >
    {children}
  </button>
)

export default function ImageGenerator() {
  const [loading, setLoading] = useState(false)
  const [image, setImage] = useState(null)
  const [prompt, setPrompt] = useState('a picture of a person with a strawberry face in a city')
  const [version, setVersion] = useState('v3')

  const [improvedPrompt, setImprovedPrompt] = useState('');
  const [loraStrength, setLoraStrength] = useState(1)

  const generateImage = async () => {
    setLoading(true)
    let url = "https://warpvideoai--all-luma-endpoints.modal.run"
    let body = {
      prompt: prompt, 
      version: version
    }
    if(version == "v3"){
      body.strength = loraStrength
    }
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()
      setImage(data.url)
      if (data.prompt) {
        setImprovedPrompt(data.prompt)
        // setPrompt(data.prompt)
      }
    } catch (error) {
      console.error('Error generating image:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePromptChange = (e) => {
    setPrompt(e.target.value)
  }
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Fruit Image Generator</h1>
      <div className="bg-gray-100 p-4 rounded-lg mb-6">
        <p className="text-sm text-gray-700 mb-2">
          <strong>V1:</strong> Base Flux Schnell with no LLM prompt improvement
        </p>
        <p className="text-sm text-gray-700">
          <strong>V2:</strong> Flux Schnell with an LLM (gpt 4o) to improve the prompt.
        </p>
        <p className="text-sm text-gray-700">
          <strong>V3:</strong> Flux Dev with the Lora I trained (so a little slower).
        </p>
        <div className="flex items-center justify-start md:justify-end mt-4 space-x-4">
          <a
            href="https://drive.google.com/file/d/1nIcBAo6dQ10FjhZK8d3hwD9Zmw-w6bbp/view?usp=sharing"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-150"
          >
            <svg className="mr-2 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
            Lora Dataset
          </a>
          <a
            href="https://github.com/saketh12/luma"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-150"
          >
            <svg className="mr-2 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
            Github
          </a>
        </div>
        
      </div>
      <div className="space-y-4">
        <Input
          type="text"
          placeholder="Enter your prompt"
          value={prompt}
          onChange={handlePromptChange}
          className="w-full"
        />
        <Select value={version} onValueChange={setVersion}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select version" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="v1">V1</SelectItem>
            <SelectItem value="v2">V2</SelectItem>
            <SelectItem value="v3">V3</SelectItem>
          </SelectContent>
        </Select>
        {version === "v3" && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium">Lora Strength</h4>
            <input
              type="range"
              min="0"
              max="4"
              step="0.1"
              value={loraStrength}
              onChange={(e) => setLoraStrength(parseFloat(e.target.value))}
              className="w-full"
            />
            <p className="text-sm text-gray-500">Current strength: {loraStrength.toFixed(1)}</p>
          </div>
        )}
        <Button
          onClick={generateImage}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate'}
        </Button>
        {version === "v2" &&
          <p className="text-sm text-gray-700">
            {improvedPrompt}
          </p>
        }
        {image && (
          <div className="mt-4 flex justify-center">
            <img src={image} alt="Generated image" className="w-full max-w-2xl object-contain" />
          </div>
        )}
      </div>
    </div>
  )
}