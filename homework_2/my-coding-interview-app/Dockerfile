# Step 1: Use the official Node.js image as a base
FROM node:16-alpine

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Step 4: Copy the rest of the application files
COPY . .

# Step 5: Expose the port
EXPOSE 5000

# Step 6: Command to run the application
CMD ["npm", "run", "dev"]
