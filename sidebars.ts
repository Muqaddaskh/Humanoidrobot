import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Custom sidebar for the PhysicalAI Humanoid Robotics Textbook
  textbookSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro'],
    },
    {
      type: 'category',
      label: 'Chapter 1: Fundamentals of Robotics',
      items: ['ch1-fundamentals'],
    },
    {
      type: 'category',
      label: 'Chapter 2: Kinematics and Dynamics',
      items: ['ch2-kinematics'],
    },
    {
      type: 'category',
      label: 'Chapter 3: Control Systems',
      items: ['ch3-control'],
    },
    {
      type: 'category',
      label: 'Chapter 4: Sensors and Perception',
      items: ['ch4-sensors'],
    },
    {
      type: 'category',
      label: 'Chapter 5: AI and Machine Learning in Robotics',
      items: ['ch5-ai-ml'],
    },
    {
      type: 'category',
      label: 'Chapter 6: Humanoid Robot Design',
      items: ['ch6-humanoid-design'],
    },
    {
      type: 'category',
      label: 'Chapter 7: Motion Planning and Locomotion',
      items: ['ch7-motion-planning'],
    },
    {
      type: 'category',
      label: 'Chapter 8: Applications and Future Directions',
      items: ['ch8-applications'],
    },
  ],
};

export default sidebars;
