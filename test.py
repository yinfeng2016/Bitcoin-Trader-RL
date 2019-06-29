import gym
import optuna
import pandas as pd

from stable_baselines.common.policies import MlpLnLstmPolicy
from stable_baselines.common.vec_env import SubprocVecEnv, DummyVecEnv
from stable_baselines import A2C, ACKTR, PPO2

from env.BitcoinTradingEnv import BitcoinTradingEnv
from util.indicators import add_indicators

curr_idx = 3
reward_strategy = 'sortino'
input_data_file = 'binance.csv'
params_db_file = 'sqlite:///params.db'

study_name = 'ppo2_' + reward_strategy
study = optuna.load_study(study_name=study_name, storage=params_db_file)
params = study.best_trial.params

print("Testing PPO2 agent with params:", params)
print("Best trial:", -1 * study.best_trial.value)

df_init = pd.read_csv('binance.csv')
# df = df.drop(['Symbol'], axis=1)
df_init = df_init.sort_values(['Date'])
df_init = add_indicators(df_init.reset_index())

test_len = int(len(df_init) * 0.021)
train_len = int(len(df_init)) - test_len

# test_df = df_init[train_len:]
test_df = df_init[16400:]
print('before load test_env')
test_env = DummyVecEnv([lambda: BitcoinTradingEnv(
    test_df, reward_func=reward_strategy, forecast_len=int(params['forecast_len']), confidence_interval=params['confidence_interval'])])
print('after load test_env')
# test_env = DummyVecEnv([lambda: BitcoinTradingEnv(
# test_df, reward_func=reward_strategy, forecast_len=4, confidence_interval=0.81)])





model_params = {
    'n_steps': int(params['n_steps']),
    'gamma': params['gamma'],
    'learning_rate': params['learning_rate'],
    'ent_coef': params['ent_coef'],
    'cliprange': params['cliprange'],
    'noptepochs': int(params['noptepochs']),
    'lam': params['lam'],
}

model = PPO2.load('./agents/ppo2_' + reward_strategy + '_' + str(curr_idx) + '_6' +  '.pkl', env=test_env)

while true: 
    df_init = pd.read_csv('binance.csv')
    # df = df.drop(['Symbol'], axis=1)
    df_init = df_init.sort_values(['Date'])
    df_init = add_indicators(df_init.reset_index())

    test_len = int(len(df_init) * 0.021)
    train_len = int(len(df_init)) - test_len

    test_df = df_init[16400:]
    print('before load test_env')
    test_env = DummyVecEnv([lambda: BitcoinTradingEnv(
        test_df, reward_func=reward_strategy, forecast_len=int(params['forecast_len']), confidence_interval=params['confidence_interval'])])
    print('after load test_env')

    obs, done = test_env.reset(), False
    while not done:
        action, _states = model.predict(obs)
        obs, reward, done, info = test_env.step(action)
        test_env.render(mode="system")
    time.sleep(10)