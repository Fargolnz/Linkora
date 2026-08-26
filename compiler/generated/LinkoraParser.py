# Generated from Linkora.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,12,49,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,5,
        0,14,8,0,10,0,12,0,17,9,0,1,0,1,0,1,1,1,1,1,1,5,1,24,8,1,10,1,12,
        1,27,9,1,1,1,1,1,1,2,1,2,3,2,33,8,2,1,3,1,3,1,3,1,3,3,3,39,8,3,1,
        4,1,4,1,4,1,4,3,4,45,8,4,1,5,1,5,1,5,0,0,6,0,2,4,6,8,10,0,1,1,0,
        1,2,49,0,15,1,0,0,0,2,20,1,0,0,0,4,32,1,0,0,0,6,34,1,0,0,0,8,44,
        1,0,0,0,10,46,1,0,0,0,12,14,3,2,1,0,13,12,1,0,0,0,14,17,1,0,0,0,
        15,13,1,0,0,0,15,16,1,0,0,0,16,18,1,0,0,0,17,15,1,0,0,0,18,19,5,
        0,0,1,19,1,1,0,0,0,20,21,5,7,0,0,21,25,5,3,0,0,22,24,3,4,2,0,23,
        22,1,0,0,0,24,27,1,0,0,0,25,23,1,0,0,0,25,26,1,0,0,0,26,28,1,0,0,
        0,27,25,1,0,0,0,28,29,5,4,0,0,29,3,1,0,0,0,30,33,3,6,3,0,31,33,3,
        2,1,0,32,30,1,0,0,0,32,31,1,0,0,0,33,5,1,0,0,0,34,35,5,8,0,0,35,
        36,5,5,0,0,36,38,3,8,4,0,37,39,5,6,0,0,38,37,1,0,0,0,38,39,1,0,0,
        0,39,7,1,0,0,0,40,45,5,9,0,0,41,45,5,10,0,0,42,45,3,10,5,0,43,45,
        5,8,0,0,44,40,1,0,0,0,44,41,1,0,0,0,44,42,1,0,0,0,44,43,1,0,0,0,
        45,9,1,0,0,0,46,47,7,0,0,0,47,11,1,0,0,0,5,15,25,32,38,44
    ]

class LinkoraParser ( Parser ):

    grammarFileName = "Linkora.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'true'", "'false'", "'{'", "'}'", "':'", 
                     "','" ]

    symbolicNames = [ "<INVALID>", "TRUE", "FALSE", "LCURLY", "RCURLY", 
                      "COLON", "COMMA", "BLOCK_NAME", "IDENTIFIER", "STRING", 
                      "NUMBER", "LINE_COMMENT", "WS" ]

    RULE_document = 0
    RULE_block = 1
    RULE_blockContent = 2
    RULE_property = 3
    RULE_value = 4
    RULE_booleanLiteral = 5

    ruleNames =  [ "document", "block", "blockContent", "property", "value", 
                   "booleanLiteral" ]

    EOF = Token.EOF
    TRUE=1
    FALSE=2
    LCURLY=3
    RCURLY=4
    COLON=5
    COMMA=6
    BLOCK_NAME=7
    IDENTIFIER=8
    STRING=9
    NUMBER=10
    LINE_COMMENT=11
    WS=12

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class DocumentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(LinkoraParser.EOF, 0)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LinkoraParser.BlockContext)
            else:
                return self.getTypedRuleContext(LinkoraParser.BlockContext,i)


        def getRuleIndex(self):
            return LinkoraParser.RULE_document

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDocument" ):
                listener.enterDocument(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDocument" ):
                listener.exitDocument(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDocument" ):
                return visitor.visitDocument(self)
            else:
                return visitor.visitChildren(self)




    def document(self):

        localctx = LinkoraParser.DocumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_document)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==7:
                self.state = 12
                self.block()
                self.state = 17
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 18
            self.match(LinkoraParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BLOCK_NAME(self):
            return self.getToken(LinkoraParser.BLOCK_NAME, 0)

        def LCURLY(self):
            return self.getToken(LinkoraParser.LCURLY, 0)

        def RCURLY(self):
            return self.getToken(LinkoraParser.RCURLY, 0)

        def blockContent(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(LinkoraParser.BlockContentContext)
            else:
                return self.getTypedRuleContext(LinkoraParser.BlockContentContext,i)


        def getRuleIndex(self):
            return LinkoraParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = LinkoraParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.match(LinkoraParser.BLOCK_NAME)
            self.state = 21
            self.match(LinkoraParser.LCURLY)
            self.state = 25
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==7 or _la==8:
                self.state = 22
                self.blockContent()
                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 28
            self.match(LinkoraParser.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def property_(self):
            return self.getTypedRuleContext(LinkoraParser.PropertyContext,0)


        def block(self):
            return self.getTypedRuleContext(LinkoraParser.BlockContext,0)


        def getRuleIndex(self):
            return LinkoraParser.RULE_blockContent

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlockContent" ):
                listener.enterBlockContent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlockContent" ):
                listener.exitBlockContent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlockContent" ):
                return visitor.visitBlockContent(self)
            else:
                return visitor.visitChildren(self)




    def blockContent(self):

        localctx = LinkoraParser.BlockContentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_blockContent)
        try:
            self.state = 32
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8]:
                self.enterOuterAlt(localctx, 1)
                self.state = 30
                self.property_()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 31
                self.block()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(LinkoraParser.IDENTIFIER, 0)

        def COLON(self):
            return self.getToken(LinkoraParser.COLON, 0)

        def value(self):
            return self.getTypedRuleContext(LinkoraParser.ValueContext,0)


        def COMMA(self):
            return self.getToken(LinkoraParser.COMMA, 0)

        def getRuleIndex(self):
            return LinkoraParser.RULE_property

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProperty" ):
                listener.enterProperty(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProperty" ):
                listener.exitProperty(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProperty" ):
                return visitor.visitProperty(self)
            else:
                return visitor.visitChildren(self)




    def property_(self):

        localctx = LinkoraParser.PropertyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_property)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            self.match(LinkoraParser.IDENTIFIER)
            self.state = 35
            self.match(LinkoraParser.COLON)
            self.state = 36
            self.value()
            self.state = 38
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 37
                self.match(LinkoraParser.COMMA)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(LinkoraParser.STRING, 0)

        def NUMBER(self):
            return self.getToken(LinkoraParser.NUMBER, 0)

        def booleanLiteral(self):
            return self.getTypedRuleContext(LinkoraParser.BooleanLiteralContext,0)


        def IDENTIFIER(self):
            return self.getToken(LinkoraParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return LinkoraParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = LinkoraParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_value)
        try:
            self.state = 44
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9]:
                self.enterOuterAlt(localctx, 1)
                self.state = 40
                self.match(LinkoraParser.STRING)
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 2)
                self.state = 41
                self.match(LinkoraParser.NUMBER)
                pass
            elif token in [1, 2]:
                self.enterOuterAlt(localctx, 3)
                self.state = 42
                self.booleanLiteral()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 4)
                self.state = 43
                self.match(LinkoraParser.IDENTIFIER)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRUE(self):
            return self.getToken(LinkoraParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(LinkoraParser.FALSE, 0)

        def getRuleIndex(self):
            return LinkoraParser.RULE_booleanLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanLiteral" ):
                listener.enterBooleanLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanLiteral" ):
                listener.exitBooleanLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBooleanLiteral" ):
                return visitor.visitBooleanLiteral(self)
            else:
                return visitor.visitChildren(self)




    def booleanLiteral(self):

        localctx = LinkoraParser.BooleanLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_booleanLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            _la = self._input.LA(1)
            if not(_la==1 or _la==2):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





