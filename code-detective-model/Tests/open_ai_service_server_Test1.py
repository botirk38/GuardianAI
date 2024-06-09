import sys
sys.path.insert(0, '../')
import grpc
import Open_servce_pb2
import Open_servce_pb2_grpc

def run():
    CODE_SAMPLE = ("use std::ptr; fn use_after_free() { let mut data = Box::new(42); let ptr = Box::into_raw(data); unsafe { ptr::drop_in_place(ptr); println!("", *ptr); } } fn main() { use_after_free(); }")
    channel = grpc.insecure_channel('localhost:50051')
    stub = Open_servce_pb2_grpc.AnalyzerStub(channel)
    request = Open_servce_pb2.AnalyzeRequest(features_json=CODE_SAMPLE)
    response = stub.AnalyzeContract(request)
    print(response)

if __name__ == '__main__':
    run()