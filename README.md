# pyppy - pipelining library
## warning - construction site
Just a friendly warning here that *pyppy* is under construction at the moment. This 
means that we might introduce breaking changes and possibly also complete refactorings at any point in
time currently. 
## what is it?
What is *pyppy*? An easy pipelining and configuration handling library for Python. 
It is meant to be used in conjunction with *argparse*'s ArgumentParser but might also 
be used with other command line and configuration utilities. 

Where *pyppy* helps the most are cases where you want your project configuration available in
many parts of your code without passing around arguments and objects from function to function.

Here is an example of what *pyppy* can do for you:
```python

```


## possible enhancements
* Debug option for container
    * Container logs every action done on it 

## known bugs
* fill_arguments decorator won't work with non-global containers (containers that
are stored with a name on first creation)
* kwargs conditions (conditions specified via kwargs) currently don't support containers

## todos
* check boolean expressions; check always if None or not None where no booleans
are expected to avoid wrong checks
* check if custom configs work (objects holding just instance attributes)
* possibility to specify arguments for pipeline steps that must be filled in runtime
(add args after pipeline has been created)
    * imagine different pipeline runs with one arg changing 