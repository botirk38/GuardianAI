# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Open_servce.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11Open_servce.proto\x12\x06openai\"\"\n\x12\x41nalyzeCodeRequest\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\".\n\x13\x41nalyzeCodeResponse\x12\x17\n\x0fvulnerabilities\x18\x01 \x01(\t2Y\n\rOpenAIService\x12H\n\x0b\x41nalyzeCode\x12\x1a.openai.AnalyzeCodeRequest\x1a\x1b.openai.AnalyzeCodeResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Open_servce_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ANALYZECODEREQUEST']._serialized_start=29
  _globals['_ANALYZECODEREQUEST']._serialized_end=63
  _globals['_ANALYZECODERESPONSE']._serialized_start=65
  _globals['_ANALYZECODERESPONSE']._serialized_end=111
  _globals['_OPENAISERVICE']._serialized_start=113
  _globals['_OPENAISERVICE']._serialized_end=202
# @@protoc_insertion_point(module_scope)
