import environment
from agent import PPOAgent
from torch.distributions import Categorical
import torch
import pygame
import sys

def evaluate_model(model_path, episodes=3, max_steps=350):
    env = environment.CollectorEnv(render=True)
    agent = PPOAgent(env)
    agent.load_model(model_path)
    agent.policy.eval()
    
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        for _ in range(max_steps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    env.close()
                    sys.exit()
            
            state_tensor = torch.FloatTensor(state).to('cuda')
            with torch.no_grad():
                probs, _ = agent.policy(state_tensor)
            action = torch.argmax(probs).item()
            
            next_state, reward, done, _ = env.step(action)
            total_reward += reward
            state = next_state
            
            # tiny delay 10ms for the rendering to keep up
            env.render()
            pygame.time.wait(10) 
            
            if done:
                break
        
        print(f"Episode {episode+1}: Reward = {total_reward}")
    
    env.close()
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: python evaluate.py <model_path>") # Adjust model path TO DO: make it a parameter
        sys.exit(1)
    
    evaluate_model(sys.argv[1])