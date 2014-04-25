import unittest
from cursesgame import pubsub

class TestPubsub(unittest.TestCase):

    def tearDown(self):
        pubsub.reset()

    def testBasic(self):
        self.called = False
        def cb():
            self.called = True

        pubsub.sub("test", cb)
        pubsub.pub("test")

        self.assertTrue(self.called)

    def testWithArgs(self):
        self.content = ""
        def cb(arg):
            self.content = arg
        pubsub.sub("test", cb)

        pubsub.pub("test", "content")
        self.assertEqual(self.content, "content")

        pubsub.pub("test", {1:1})
        self.assertEqual(self.content, {1:1})

    def testWithKwargs(self):
        self.foo, self.bar = None, None
        def cb(f, b):
            self.foo = f
            self.bar = b
        pubsub.sub("test", cb)

        pubsub.pub("test", f=1, b=2)
        self.assertEqual(self.foo, 1)
        self.assertEqual(self.bar, 2)

        pubsub.pub("test", b=1, f=2)
        self.assertEqual(self.bar, 1)
        self.assertEqual(self.foo, 2)

    def testUnsub(self):
        self.called = False
        def cb():
            self.called = True
        pubsub.sub("test", cb)

        pubsub.pub("test")
        self.assertTrue(self.called)

        self.called = False
        pubsub.unsub("test", cb)
        pubsub.pub("test")
        self.assertFalse(self.called)

if __name__ == '__main__':
   unittest.main()

