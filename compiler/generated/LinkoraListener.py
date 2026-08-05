# Generated from Linkora.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LinkoraParser import LinkoraParser
else:
    from LinkoraParser import LinkoraParser

# This class defines a complete listener for a parse tree produced by LinkoraParser.
class LinkoraListener(ParseTreeListener):

    # Enter a parse tree produced by LinkoraParser#document.
    def enterDocument(self, ctx:LinkoraParser.DocumentContext):
        pass

    # Exit a parse tree produced by LinkoraParser#document.
    def exitDocument(self, ctx:LinkoraParser.DocumentContext):
        pass


    # Enter a parse tree produced by LinkoraParser#block.
    def enterBlock(self, ctx:LinkoraParser.BlockContext):
        pass

    # Exit a parse tree produced by LinkoraParser#block.
    def exitBlock(self, ctx:LinkoraParser.BlockContext):
        pass


    # Enter a parse tree produced by LinkoraParser#blockContent.
    def enterBlockContent(self, ctx:LinkoraParser.BlockContentContext):
        pass

    # Exit a parse tree produced by LinkoraParser#blockContent.
    def exitBlockContent(self, ctx:LinkoraParser.BlockContentContext):
        pass


    # Enter a parse tree produced by LinkoraParser#property.
    def enterProperty(self, ctx:LinkoraParser.PropertyContext):
        pass

    # Exit a parse tree produced by LinkoraParser#property.
    def exitProperty(self, ctx:LinkoraParser.PropertyContext):
        pass


    # Enter a parse tree produced by LinkoraParser#value.
    def enterValue(self, ctx:LinkoraParser.ValueContext):
        pass

    # Exit a parse tree produced by LinkoraParser#value.
    def exitValue(self, ctx:LinkoraParser.ValueContext):
        pass


    # Enter a parse tree produced by LinkoraParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:LinkoraParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by LinkoraParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:LinkoraParser.BooleanLiteralContext):
        pass



del LinkoraParser