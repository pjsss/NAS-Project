import json
import time
import random
import os
from multiprocessing import Queue, Pool
from tensorflow import set_random_seed

import corenas
from enumerater import Enumerater
from communicator import Communicator
from evaluator import Evaluator
from info_str import (
    CUR_VER_DIR,
    NAS_CONFIG_PATH,
    EVALOG_PATH_TEM,
    NETWORK_INFO_PATH,
    WINNER_LOG_PATH,
    LOG_EVAINFO_TEM,
    LOG_EVAFAIL,
    LOG_WINNER_TEM,
    SYS_EVAFAIL,
    SYS_EVA_RESULT_TEM,
    SYS_ELIINFO_TEM,
    SYS_INIT_ING,
    SYS_I_AM_PS,
    SYS_I_AM_WORKER,
    SYS_ENUM_ING,
    SYS_SEARCH_BLOCK_TEM,
    SYS_WORKER_DONE,
    SYS_WAIT_FOR_TASK,
    SYS_CONFIG_ING,
    SYS_GET_WINNER,
    SYS_BEST_AND_SCORE_TEM,
    SYS_START_GAME_TEM,
    SYS_CONFIG_OPS_ING
)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Global variables
NAS_CONFIG = json.load(open(NAS_CONFIG_PATH, encoding='utf-8'))
IDLE_GPUQ = Queue()

def _gpu_eva(params):
    graph, cell, nn_pb, _, p_, ft_sign, pl_, eva, ngpu = params
    # params = (graph, cell, nn_preblock, round, pos,
    # finetune_signal, pool_len, eva, ngpu)
    start_time = time.time()

    os.environ['CUDA_VISIBLE_DEVICES'] = str(params.ngpu)
    with open(EVALOG_PATH_TEM.format(ngpu)) as f:
        f.write(LOG_EVAINFO_TEM.format(
            len(nn_pb)+1, round, p_, pl_
        ))
        while True:
            try:
                score = eva.evaluate(graph, cell, nn_pb, False, ft_sign, f)
                break
            except:
                print(SYS_EVAFAIL)
                f.write(LOG_EVAFAIL)
        IDLE_GPUQ.put(ngpu)

    end_time = time.time()
    start_time = time.time()
    time_cost = end_time - start_time
    return score, time_cost, p_


def _module_init():
    enu = Enumerater(
        depth=NAS_CONFIG["depth"],
        width=NAS_CONFIG["width"],
        max_branch_depth=NAS_CONFIG["max_depth"])
    eva = Evaluator()

    return enu, eva

def _filln_queue(q, n):
    for i in range(n):
        q.put(i)

def _wait_for_event(event_func):
    # TODO replaced by multiprocessing.Event
    while event_func():
        print(SYS_WAIT_FOR_TASK)
        time.sleep(20)
    return

class Nas():
    def __init__(self, job_name, ps_host=''):
        self.__is_ps = (job_name == 'ps')
        self.__ps_host = ps_host

        set_random_seed(NAS_CONFIG["randseed"])
        return

    def __ps_run(self, enum, eva, cmnct):
        _filln_queue(IDLE_GPUQ, NAS_CONFIG["num_gpu"])
        print(SYS_ENUM_ING)
        network_pool_tem = enum.enumerate()

        for i in range(NAS_CONFIG["block_num"]):
            print(SYS_SEARCH_BLOCK_TEM.format(i+1, NAS_CONFIG["block_num"]))
            block, best_index = corenas.Corenas(i, eva, cmnct, network_pool_tem)
            block.pre_block.append([
                block.graph_part,
                block.graph_full_list[best_index],
                block.cell_list[best_index]
            ])
        cmnct.end_flag.put(1) # TODO find other way to stop workers

        return block.pre_block

    # TODO ps -> worker
    # @staticmethod
    def __worker_run(self, eva, cmnct):
        _filln_queue(IDLE_GPUQ, NAS_CONFIG["num_gpu"])
        pool = Pool(processes=NAS_CONFIG["num_gpu"])
        while cmnct.end_flag.empty():
            _wait_for_event(cmnct.data_sync.empty)

            cmnct.data_count += 1
            data_count_ps = cmnct.data_sync.get(timeout=1)
            eva.add_data(1600*(data_count_ps-cmnct.data_count+1))
            result_list = []

            while not cmnct.task.empty():
                gpu = IDLE_GPUQ.get()
                try:
                    task_params = cmnct.task.get(timeout=1)
                except:
                    IDLE_GPUQ.put(gpu)
                    break
                result = pool.apply_async(_gpu_eva, args=task_params)
                result_list.append(result)
            for r_ in result_list:
                score, time_cost, network_index = r_.get()
                print(SYS_EVA_RESULT_TEM.format(network_index, score, time_cost))
                cmnct.result.put([score, network_index, time_cost])

            _wait_for_event(cmnct.task.empty)
        pool.close()
        pool.join()
        return

    def run(self):
        print(SYS_INIT_ING)
        enum, eva = _module_init()
        cmnct = Communicator(self.__is_ps, self.__ps_host)
        if self.__is_ps:
            print(SYS_I_AM_PS)
            return self.__ps_run(enum, eva, cmnct)
        else:
            print(SYS_I_AM_WORKER)
            self.__worker_run(eva, cmnct)
            print(SYS_WORKER_DONE)

        return

if __name__ == '__main__':
    nas = Nas('ps', '127.0.0.1:5000')
    nas.run()