"""Code Review
1) You are missing all the docstings for all classes and methods, I highly
recommend to use the Google Docstrings Style
"""
import datetime as dt


class Record:
    """Code Review: Record class for adding new element to a calculator

    Notes:
        1) According to PEP 257 - Docstring Conventions, the __init__
        constructor should also have docstring, especially since your date
        argument requires more clarification on the expected string format
        with an example and the type hints, see correction below.
        2) A more pythonic way to define an empty argument is using None
        instead of an empty string or a list; since it is a singleton,
        your compare it using 'date is None' which is actually faster than
        'date == None'.
        3) Alternatively, you could have written your function the next way:

        today = dt.datetime.today().strftime('%d.%m.%Y')

        def __init__(self, amount: float, comment: str, date: str = today):
            self.amount = amount
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
            self.comment = comment

        This way you avoid the if one liner keeping consistecy in the string
        type for date having always available a date to parse.
    """
    def __init__(self, amount: float, comment: str, date: str = None):
        """Record Constructor

        Args:
            amount (float): Number (monetary amount or number of calories)
            comment (str): Explaining what the money was spent on or where
            the calories came from
            date (str, optional): Creation date, i.e. 03.01.2021.
            Defaults to None.
        """
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            date is None
            else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    """Code Review: Calculator Class
    1) Be careful with docstings and type hints.
    """
    def __init__(self, limit: float):
        """Calculator Constructor
        1) In the case of money, limit should be given by default in
        a currency, according to your assignment, it would be Ruples

        Args:
            limit (float): Limit for money in Rubles or calories usage
        """
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        """Code Review: Add a new record
        1) Here is really important the usage of the type hint pointing
        to your Record class for clarification.

        Args:
            record (Record): Record object
        """
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Code Review: Get Today Stats
        1) Type Hint added '-> float' for specifying return
        2) 'Record' in loop might generate confusions that you
        are referring to the Record class, but it is actually to an
        element from the self.records list; also, it is not
        compliant with standards as variables should never start
        with capitals.
        3) Rewrite your sum in the following way:
            today_stats += record.amount
        4) You can also refactor your function as a comprehension sum,
        which is the best pythonic way to do it:

        today = dt.datetime.now().date()
        today_stats = sum(record.amount for record in self.records
                          if record.date == today)
        return today_stats

        Returns:
            float: Total sum of records' amounts for today
        """
        today_stats = 0
        for record in self.records:
            if record.date == dt.datetime.now().date():
                today_stats = today_stats + record.amount
        return today_stats

    def get_week_stats(self) -> float:
        """Code Review: Get Week Stats
        1) Type Hint added '-> float' for specifying return
        2) You can also refactor your function as a comprehension sum,
        which is the best pythonic way to do it:

        today = dt.datetime.now().date()
        week_stats = sum(record.amount for record in self.records
                         if (today - record.date).days < 7)
        return week_stats

        Denote that comparison with '0' is removed since the difference
        will always be positive as it is today against previous days,
        not future ones. In any case, when a Record is created, the class
        may need a way to prevent entering future dates.

        Returns:
            float: Total sum of records' amounts for this week
        """
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    """Code Review: Calories Calculator

    Args:
        Calculator (class): Inheritance from Calculator class
    """
    def get_calories_remained(self) -> str:  # Gets the remaining calories for today
        """Code Review: Get calories calories_remnant
        1) Type Hint added '-> float' for specifying return
        2) Comment from line 136 should be inside this docstring
        3) Name for variable 'x' is not compliant with standards,
        it should be a representative English word, i.e. calories_remnant
        4) Unnecessary else condition since it is only a return
        5) Last 'return' does not require parens since it is not a
        multiline string
        6) 'if calories_remnant > 0:' can be rewritten as
        'if calories_remnant:', as calories_remnant will be
        True as long as it is not zero.
        7) f-string can be refactored using brackets as below
        to avoid the backslash
        8) Incorrect message when the limit is not reached:
        'Today you can eat some more, but with a total calorie
        content of no more than N kcal'

        Returns:
            str: Notification status for calories calories_remnant
        """
        calories_remnant = self.limit - self.get_today_stats()
        if calories_remnant:
            return (f'Today you can eat some more, '
                    f'but with a total calorie content'
                    f'of no more than {calories_remnant} kcal')
        return 'Stop eating!'


class CashCalculator(Calculator):
    """Code Review: Cash Calculator class

    Args:
        Calculator (class): Inheritance from Calculator class
    """
    USD_RATE = float(60)  # US dollar exchange rate.
    EURO_RATE = float(70)  # Euro exchange rate.

    def get_today_cash_remained(self, currency_sel: str):
        """Code Review: Get cash remnant for today
        1) USD_RATE and EURO_RATE can be accessed through the 'self' command;
        therefore, they can be removed from the method arguments.
        2) Type hint and expected example for currency
        3) currency assignment to currency_type is not necessary
        4) The currency string and conversion rate could be better
        handled with a dict of tuples as in the following refactoring.
        5) 'cash_remained' for rub is wrongly used as it is not working
        as a rate but as a direct assignment to 1
        6) Incorrect output messages for the 3 scenarios
        7) In 'f'Left for today {round(cash_remained, 2)} ' it is better
        to have done the round outside the f-string and only pass the value
        already rounded.
        8) In the final return. the usage of the '.format' is now deprecated
        by f-strings to present a more readable and clean code.
        9) Given the 3 currencies available, you may have to handle with errors
        when trying to use another currencies not available.
        10) The refactoring is done in place, please check against your
        original solution

        Args:
            currency_sel (str): Currency selection, i.e. "rub", "usd" or "eur"

        Returns:
            string: Notification status for calories cash_remained
        """
        currency_types = {
            'rub': (1, 'Rubles'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
        }
        cash_remained = self.limit - self.get_today_stats()
        rate, currency_str = currency_types[currency_sel]
        cash_remained = round(cash_remained / rate, 2)
        if cash_remained > 0:
            return f'There are {cash_remained} {currency_str} left for today'
        if cash_remained == 0:
            return 'There is no money, stay strong'
        return (f'There is no money, stay strong: '
                f'your debt is {cash_remained} {currency_str}')

    def get_week_stats(self):
        """The intent of this function was to override it, however
        since no changes are done to the parent method, this
        override intent can be discarded
        """
        super().get_week_stats()
