#python
from saleae.analyzers import LogicAnalyzerAnalyzer, Version 

my_version = Version(1, 0, 0)

class Analyzer(LogicAnalyzerAnalyzer): 
    version = my_version
    
    def __init__(self): 
        pass
    
    def process_captured_data(self):
        sampling_rate = self.manager.session.ch1_minimum_sample_rate 
        data = self.manager.get_buffer('CH1')
        
        # 定义协议格式
        # 每个bit时间长度 = 1/sampling_rate * 100 
        bit_time = int(sampling_rate * 100)  
        
        # 帧开始标志,2个bit 1 
        frame_start = [1,1] 
        
        # 解码后的数据和时间
        results = []     
        times = []     
        
        # 扫描捕获数据 
        for i in range(len(data) - len(frame_start)*bit_time):
            # 检测帧开始标志
            if data[i:i+2*bit_time] == frame_start:  
                # 读取数据,8个bit长度  
                value = 0     
                for j in range(0,8*bit_time,bit_time):  
                    value = (value << 1) | data[i+2*bit_time+j]     
                # 添加解码结果和时间         
                results.append(value)
                times.append(i)
        
        # 显示解码结果
        for value,time in zip(results,times):
            self.add_result(time,"Data:{0}".format(value))
