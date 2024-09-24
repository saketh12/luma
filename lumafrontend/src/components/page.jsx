'use client'

import { useState } from 'react'
import { Input } from "@/components/ui/input"
import { Checkbox } from "@/components/ui/checkbox"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"

export function Page() {
  const [activeTab, setActiveTab] = useState('v1')

  const TabContent = () => (
    <div className="space-y-4 p-4">
      <h2 className="text-2xl font-bold">Tab: {activeTab}</h2>
      <Input type="text" placeholder="Enter your prompt" />
      <div className="flex items-center space-x-2">
        <Checkbox id="realism" />
        <label htmlFor="realism">Use realism lora</label>
      </div>
      <Select>
        <SelectTrigger>
          <SelectValue placeholder="Select size" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="square">Square</SelectItem>
          <SelectItem value="square_hd">Square HD</SelectItem>
        </SelectContent>
      </Select>
    </div>
  )

  return (
    (<div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Simple Image Generator</h1>
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="v1">V1</TabsTrigger>
          <TabsTrigger value="v2">V2</TabsTrigger>
          <TabsTrigger value="v3">V3</TabsTrigger>
        </TabsList>
        <TabsContent value="v1"><TabContent /></TabsContent>
        <TabsContent value="v2"><TabContent /></TabsContent>
        <TabsContent value="v3"><TabContent /></TabsContent>
      </Tabs>
    </div>)
  );
}