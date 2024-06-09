import sys
sys.path.insert(0, '../')
import grpc
import Open_servce_pb2
import Open_servce_pb2_grpc

def run():
    CODE_SAMPLE = ("use ink_lang as ink; #[ink::contract] mod my_contract { use super::*; #[ink(storage)] pub struct MyContract { value: Balance, } impl MyContract { #[ink(constructor)] pub fn new(init_value: Balance) -> Self { Self { value: init_value } } #[ink(message, payable)] pub fn donate(&mut self) { self.value += self.env().transferred_balance(); } #[ink(message)] pub fn withdraw(&mut self, amount: Balance) { if self.value >= amount { self.env().transfer(self.env().caller(), amount).expect(\"Transfer failed\"); self.value -= amount; } } #[ink(message)] pub fn get_balance(&self) -> Balance { self.value } } }")
    channel = grpc.insecure_channel('localhost:50051')
    stub = Open_servce_pb2_grpc.AnalyzerStub(channel)
    request = Open_servce_pb2.AnalyzeRequest(features_json=CODE_SAMPLE)
    response = stub.AnalyzeContract(request)
    print(response)

if __name__ == '__main__':
    run()