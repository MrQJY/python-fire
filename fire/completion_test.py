# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the completion module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from fire import completion
from fire import test_components as tc
from fire import testutils


class TabCompletionTest(testutils.BaseTestCase):

  def testCompletionScript(self):
    # A sanity check test to make sure the completion script satisfies some
    # basic assumptions.
    commands = [
        ['run'],
        ['halt'],
        ['halt', '--now'],
    ]
    script = completion._Script(name='command', commands=commands)  # pylint: disable=protected-access
    self.assertIn('command', script)
    self.assertIn('halt', script)
    self.assertIn('"$start" == "command"', script)

  def testFnCompletions(self):
    def example(one, two, three):
      return one, two, three

    completions = completion.Completions(example)
    self.assertIn('--one', completions)
    self.assertIn('--two', completions)
    self.assertIn('--three', completions)

  def testListCompletions(self):
    completions = completion.Completions(['red', 'green', 'blue'])
    self.assertIn('0', completions)
    self.assertIn('1', completions)
    self.assertIn('2', completions)
    self.assertNotIn('3', completions)

  def testDictCompletions(self):
    colors = {
        'red': 'green',
        'blue': 'yellow',
        '_rainbow': True,
    }
    completions = completion.Completions(colors)
    self.assertIn('red', completions)
    self.assertIn('blue', completions)
    self.assertNotIn('green', completions)
    self.assertNotIn('yellow', completions)
    self.assertNotIn('_rainbow', completions)
    self.assertNotIn('True', completions)
    self.assertNotIn(True, completions)

  def testDictCompletionsVerbose(self):
    colors = {
        'red': 'green',
        'blue': 'yellow',
        '_rainbow': True,
    }
    completions = completion.Completions(colors, verbose=True)
    self.assertIn('red', completions)
    self.assertIn('blue', completions)
    self.assertNotIn('green', completions)
    self.assertNotIn('yellow', completions)
    self.assertIn('_rainbow', completions)
    self.assertNotIn('True', completions)
    self.assertNotIn(True, completions)

  def testDeepDictCompletions(self):
    deepdict = {'level1': {'level2': {'level3': {'level4': {}}}}}
    completions = completion.Completions(deepdict)
    self.assertIn('level1', completions)
    self.assertNotIn('level2', completions)

  def testDeepDictScript(self):
    deepdict = {'level1': {'level2': {'level3': {'level4': {}}}}}
    script = completion.Script('deepdict', deepdict)
    self.assertIn('level1', script)
    self.assertIn('level2', script)
    self.assertIn('level3', script)
    self.assertNotIn('level4', script)  # The default depth is 3.

  def testNonStringDictCompletions(self):
    completions = completion.Completions({
        10: 'green',
        3.14: 'yellow',
        ('t1', 't2'): 'pink',
    })
    self.assertIn('10', completions)
    self.assertIn('3.14', completions)
    self.assertIn("('t1', 't2')", completions)
    self.assertNotIn('green', completions)
    self.assertNotIn('yellow', completions)
    self.assertNotIn('pink', completions)

  def testGeneratorCompletions(self):
    def generator():
      x = 0
      while True:
        yield x
        x += 1
    completions = completion.Completions(generator())
    self.assertEqual(completions, [])

  def testClassCompletions(self):
    completions = completion.Completions(tc.NoDefaults)
    self.assertEqual(completions, [])

  def testObjectCompletions(self):
    completions = completion.Completions(tc.NoDefaults())
    self.assertIn('double', completions)
    self.assertIn('triple', completions)

  def testMethodCompletions(self):
    completions = completion.Completions(tc.NoDefaults().double)
    self.assertNotIn('--self', completions)
    self.assertIn('--count', completions)


if __name__ == '__main__':
  testutils.main()
