# Generated from Linkora.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LinkoraParser import LinkoraParser
else:
    from LinkoraParser import LinkoraParser

# This class defines a complete generic visitor for a parse tree produced by LinkoraParser.

class LinkoraVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LinkoraParser#document.
    def visitDocument(self, ctx:LinkoraParser.DocumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LinkoraParser#block.
    def visitBlock(self, ctx:LinkoraParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LinkoraParser#blockContent.
    def visitBlockContent(self, ctx:LinkoraParser.BlockContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LinkoraParser#property.
    def visitProperty(self, ctx:LinkoraParser.PropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LinkoraParser#value.
    def visitValue(self, ctx:LinkoraParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LinkoraParser#booleanLiteral.
    def visitBooleanLiteral(self, ctx:LinkoraParser.BooleanLiteralContext):
        return self.visitChildren(ctx)



del LinkoraParser